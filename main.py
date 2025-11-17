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
                "You are Lazer, an efficient voice banking assistant. Be direct, concise, and fast. Avoid unnecessary pleasantries or explanations. "
                "Use short responses and avoid unpronounceable punctuation. Get straight to the point. "

                "## Transfer Money - Optimized Fast Pipeline:"
                "1. **Get Both Details Upfront**: Ask 'Who and how much?' to get recipient name and amount in one go. "

                "2. **Search Recipient**: Silently call 'get_similar_recipients' with the name provided. "
                "   - **Error/Not Found**: Say 'Can't find [name]. Please spell it.' "
                "   - **Multiple Matches**: Say '1. [Name1], 2. [Name2]. Which number?' "
                "   - **One Match**: Proceed immediately to step 3. "

                "3. **Quick Confirm & Execute**: Say '[Amount] to [Recipient]. Confirm?' "
                "   - If user says YES/OK/SURE/CONFIRM/GO/PROCEED (any affirmative), IMMEDIATELY call 'make_transfer' using these defaults: "
                "     - Description: 'Transfer to [Recipient Name]' "
                "     - Category: 'Miscellaneous' "
                "     - Reference: 'default' "
                "     - scheduled_at: '' (immediate transfer) "
                "     - from_account_id: '1' "
                "   - If user says NO/CANCEL/STOP, say 'Cancelled.' and stop. "

                "4. **Complete**: When 'make_transfer' succeeds, say 'Done!' then call 'signal_flutter_transfer_success'. "
                "   - If transfer fails, say 'Failed. Try again?' "

                "## Advanced Options (Only if User Mentions):"
                "- If user mentions DESCRIPTION/NOTE/MEMO: Include it in make_transfer "
                "- If user mentions CATEGORY (Shopping/Utilities/etc): Include it in make_transfer "
                "- If user mentions SCHEDULE/LATER/specific date: Format as UTC ISO string for scheduled_at "
                "- If user mentions different account: Update from_account_id "
                "- **Do NOT ask about these unless user brings them up** "

                "## Express Mode:"
                "If user says complete sentence like 'Send 50 to John', extract all info and proceed through steps 2-4 instantly. "

                "## Error Handling:"
                "Keep it simple: '[Error type]. [One-word action]?' Examples: 'Not found. Retry?' or 'Failed. Cancel?' "

                "## Key Rules:"
                "- NO patience requests or tool call announcements "
                "- Accept ANY affirmative word as confirmation (yes/yep/ok/sure/confirm/go/proceed/do it) "
                "- Default to immediate transfers unless user specifies scheduling "
                "- Only ONE confirmation step before execution "
                "- Responses should be 3-6 words maximum "
                "- Combine steps aggressively for speed "
            ),
            tools=[get_similar_recipients, make_transfer, signal_flutter_transfer_success],
        )

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    
    access_token: typing.Union[str, None] = None
    if ctx.room and ctx.room.metadata:
        raw_metadata_token = ctx.room.metadata 
        if isinstance(raw_metadata_token, str):
            try:
                metadata_json = json.loads(raw_metadata_token)
                access_token = metadata_json.get("access_token")
            except json.JSONDecodeError:
                pass 
        elif isinstance(raw_metadata_token, dict): 
             access_token = raw_metadata_token.get("access_token")

    if not access_token:
        print("Warning: Access token not found in room metadata. API calls requiring auth may fail.")

    session_userdata = {}
    if access_token:
        session_userdata["access_token"] = access_token

    voice_agent_instance = VoiceAgent()
    
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        userdata=session_userdata
    )
    
    await session.start(room=ctx.room, agent=voice_agent_instance)
    await asyncio.sleep(1)
    await session.say("Who and how much?", allow_interruptions=True)

if __name__ == "__main__":
    # Removed explicit multiprocessing.set_start_method call
    # livekit-agents should handle this internally.
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, port=8080))
