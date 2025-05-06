import asyncio
import os
from dotenv import load_dotenv
from livekit.agents import (
    JobContext,
    WorkerOptions,
    cli,
    llm,
    Agent,
    AgentSession,
    AutoSubscribe,
)
from livekit.plugins import openai, silero
from api import get_temperature, set_temperature
import multiprocessing

load_dotenv(dotenv_path="app.env", override=True)
print(f"DEBUG_LOAD_ENV: LIVEKIT_URL loaded: {os.getenv('LIVEKIT_URL')}")
print(f"DEBUG_LOAD_ENV: LIVEKIT_API_KEY loaded: {os.getenv('LIVEKIT_API_KEY')}")
print(f"DEBUG_LOAD_ENV: LIVEKIT_API_SECRET loaded: {os.getenv('LIVEKIT_API_SECRET')}")
print(f"DEBUG_LOAD_ENV: OPENAI_API_KEY loaded: {os.getenv('OPENAI_API_KEY')}")

# Removed fallback logic to test .env loading directly
# The Worker will pick these up from the environment if load_dotenv is successful

class VoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=(
                "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
                "You should use short and concise responses, and avoiding usage of unpronouncable punctuation. "
                "You can get and set temperatures for various rooms."
            ),
            tools=[get_temperature, set_temperature],
        )

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    voice_agent_instance = VoiceAgent()
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
    )
    await session.start(agent=voice_agent_instance, room=ctx.room)
    await asyncio.sleep(1)
    await session.say("Hey, how can I help you today!", allow_interruptions=True)

if __name__ == "__main__":
    # Try setting the start method for multiprocessing
    # This must be done before any multiprocessing-dependent code from livekit might run
    # and ideally only in the main execution block.
    try:
        multiprocessing.set_start_method('spawn', force=True)
    except RuntimeError:
        # Might have already been set, or not applicable in this context (e.g., already in a spawned process)
        pass

    # WorkerOptions does not take url, api_key, api_secret directly.
    # These must be in the environment for the Worker to pick up.
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, port=8082))
