import asyncio
import os
import json
import typing
from dotenv import load_dotenv
from livekit.agents import (
    JobContext,
    WorkerOptions,
    cli,
    llm,
    Agent,
    AgentSession,
    AutoSubscribe,
    RunContext,
)
from livekit.agents.llm import ChatMessage
from livekit.plugins import openai, silero
from api import get_similar_recipients, make_transfer, signal_flutter_transfer_success
from languages import (
    Language,
    get_greeting,
    get_instructions,
    detect_language_from_text,
    LANGUAGE_NAMES
)
import multiprocessing
import logging

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv(dotenv_path="app.env", override=True)
print(f"DEBUG_LOAD_ENV: LIVEKIT_URL loaded: {os.getenv('LIVEKIT_URL')}")
print(f"DEBUG_LOAD_ENV: LIVEKIT_API_KEY loaded: {os.getenv('LIVEKIT_API_KEY')}")
print(f"DEBUG_LOAD_ENV: LIVEKIT_API_SECRET loaded: {os.getenv('LIVEKIT_API_SECRET')}")
print(f"DEBUG_LOAD_ENV: OPENAI_API_KEY loaded: {os.getenv('OPENAI_API_KEY')}")

# Removed fallback logic to test .env loading directly
# The Worker will pick these up from the environment if load_dotenv is successful

class VoiceAgent(Agent):
    def __init__(self, language: Language = Language.ENGLISH):
        """
        Initialize voice agent with specified language support

        Args:
            language: The language to use (English, Igbo, Hausa, or Yoruba)
        """
        self.language = language
        instructions = get_instructions(language)

        logger.info(f"Initializing VoiceAgent with language: {LANGUAGE_NAMES[language]} ({language.value})")

        super().__init__(
            instructions=instructions,
            tools=[get_similar_recipients, make_transfer, signal_flutter_transfer_success],
        )

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Extract access token and language from room metadata
    access_token: typing.Union[str, None] = None
    user_language: Language = Language.ENGLISH  # Default language

    if ctx.room and ctx.room.metadata:
        raw_metadata_token = ctx.room.metadata
        if isinstance(raw_metadata_token, str):
            try:
                metadata_json = json.loads(raw_metadata_token)
                access_token = metadata_json.get("access_token")
                # Get language preference from metadata
                lang_code = metadata_json.get("language", "en")
                try:
                    user_language = Language(lang_code)
                    logger.info(f"User language from metadata: {LANGUAGE_NAMES[user_language]}")
                except ValueError:
                    logger.warning(f"Invalid language code '{lang_code}', defaulting to English")
                    user_language = Language.ENGLISH
            except json.JSONDecodeError:
                pass
        elif isinstance(raw_metadata_token, dict):
             access_token = raw_metadata_token.get("access_token")
             lang_code = raw_metadata_token.get("language", "en")
             try:
                 user_language = Language(lang_code)
                 logger.info(f"User language from metadata: {LANGUAGE_NAMES[user_language]}")
             except ValueError:
                 logger.warning(f"Invalid language code '{lang_code}', defaulting to English")
                 user_language = Language.ENGLISH

    if not access_token:
        logger.warning("Access token not found in room metadata. API calls requiring auth may fail.")

    session_userdata = {}
    if access_token:
        session_userdata["access_token"] = access_token

    # Add language to userdata for potential use in API calls
    session_userdata["language"] = user_language.value

    # Initialize voice agent with user's language
    voice_agent_instance = VoiceAgent(language=user_language)

    # ═══════════════════════════════════════════════════════════
    # PRODUCTION CONFIGURATION - Best Models for Nigerian Languages
    # ═══════════════════════════════════════════════════════════
    #
    # STT: OpenAI Whisper-large-v3 (via whisper-1 API)
    #      - Excellent multilingual STT trained on 680k hours
    #      - Native support for all 5 languages (en, pcm, ig, ha, yo)
    #      - Handles Nigerian accents and code-switching
    #      - 97+ languages supported
    #
    # LLM: GPT-4o
    #      - Best multilingual understanding
    #      - Superior Nigerian language comprehension
    #      - Fast inference (2x faster than GPT-4 Turbo)
    #      - Cost-effective ($0.003/1k input, $0.015/1k output)
    #
    # TTS: OpenAI TTS-1-HD (for best quality)
    #      - High-quality voice synthesis
    #      - Good support for all languages
    #      - NOTE: For NATIVE voices in Hausa/Yoruba, use Google Cloud TTS
    #        (see google_cloud_models.py for integration)
    # ═══════════════════════════════════════════════════════════

    # Select best TTS voice based on language with accent optimization
    tts_voice_map = {
        Language.ENGLISH: "alloy",   # Neutral, clear voice
        Language.FRENCH: "echo",     # Best for French accent (warm, sophisticated)
        Language.PIDGIN: "nova",     # Warm, conversational voice (works well for Pidgin)
        Language.IGBO: "shimmer",    # Clear, friendly voice
        Language.HAUSA: "onyx",      # Strong, clear voice
        Language.YORUBA: "fable"     # Expressive voice
    }

    selected_voice = tts_voice_map.get(user_language, "alloy")

    # Use HD model for best quality
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=openai.STT(
            model="whisper-1",  # Production-grade (whisper-large-v3 backend)
            language=user_language.value if user_language != Language.PIDGIN else "en"  # Pidgin uses 'en' hint
        ),
        llm=openai.LLM(
            model="gpt-4o",  # Best multilingual model
            temperature=0.8  # Higher temperature for natural Nigerian language responses
        ),
        tts=openai.TTS(
            voice=selected_voice,
            model="tts-1-hd"  # HD model for best quality
        ),
        userdata=session_userdata
    )

    logger.info(f"""
    ═══════════════════════════════════════════════════════════
    🎙️  PRODUCTION MODEL CONFIGURATION
    ═══════════════════════════════════════════════════════════
    Language: {LANGUAGE_NAMES[user_language]} ({user_language.value})

    🎧 STT: OpenAI Whisper-large-v3
         ✓ Best multilingual accuracy
         ✓ Native support for Nigerian languages & accents
         ✓ Handles code-switching seamlessly

    🧠 LLM: GPT-4o
         ✓ Superior multilingual understanding
         ✓ Excellent Nigerian language comprehension
         ✓ Temperature: 0.8 (natural conversations)

    🔊 TTS: OpenAI TTS-1-HD ({selected_voice})
         ✓ High-quality voice synthesis
         ✓ Clear pronunciation
         ✓ Good support for {LANGUAGE_NAMES[user_language]}

    💡 TIP: For native Hausa/Yoruba voices, see google_cloud_models.py
    ═══════════════════════════════════════════════════════════
    """)

    await session.start(room=ctx.room, agent=voice_agent_instance)
    await asyncio.sleep(1)

    # Greet user in their language
    greeting = get_greeting(user_language)
    logger.info(f"Greeting user in {LANGUAGE_NAMES[user_language]}: {greeting}")
    await session.say(greeting, allow_interruptions=True)

if __name__ == "__main__":
    # Removed explicit multiprocessing.set_start_method call
    # livekit-agents should handle this internally.
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, port=8080))
