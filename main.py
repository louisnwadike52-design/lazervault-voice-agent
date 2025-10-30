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
from api import get_temperature, set_temperature, get_similar_recipients, make_transfer, signal_flutter_transfer_success
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
                "You are a voice assistant created by LiveKit. Your name is 'Lazer'. You're a banking assistant. Your interface with users will be voice. "
                "You should use short and concise responses, and avoiding usage of unpronouncable punctuation. "
                "You are a banking assistant. You can help users transfer money. Always tell user to excersise patience letting them know when ever you need to make a tool call or search "
                
                "## Transfer Money Pipeline:"
                "1. **Get Recipient and Amount**: Start by asking 'Who would you like to send money to and how much?' This gets both pieces of essential information in one question. "
                "2. **Find Recipients Tool**: Use the 'get_similar_recipients' tool with the provided name. "
                "   - **If 'get_similar_recipients' returns an error**: Inform the user, 'I had trouble looking up that name. Could you please spell it?' "
                "   - **If no recipients are found**: Tell the user, 'I couldn\'t find anyone by that name. Could you please check the spelling?' "
                "3. **Handle Multiple Matches**: If multiple users are found, list them by number (e.g., '1. John Doe, 2. Jane Doe'). Ask 'Which one?' If their choice is ambiguous, ask 'Which John did you mean? John Doe, number 1, or John Smith, number 2?' "
                "4. **Quick Confirmation**: Once a recipient is identified, quickly confirm: 'Sending [Amount] to [Recipient Name]. Is that correct?' "
                "5. **Optional Details**: If confirmed, ask 'Would you like to add any details like description, category, reference, or schedule the transfer? If not, I'll use defaults.' "
                "   - If they say yes, ask for the specific details they want to add "
                "   - If they say no or don't respond, use defaults: "
                "     - Description: 'Transfer payment to [Recipient Name]' "
                "     - Category: 'Miscellaneous' "
                "     - Reference: 'default' "
                "     - Schedule: Immediate transfer (empty string) "
                "   - For scheduled transfers: "
                "     - If user mentions 'transfer now' or similar, use empty string for scheduled_at "
                "     - If user specifies a future date/time, format it as UTC ISO string "
                "     - Validate the datetime format before proceeding "
                "6. **Authorization**: If everything is confirmed, say 'To proceed, please say AUTHORIZE.' "
                "7. **Execute Transfer**: If they say 'AUTHORIZE', call 'make_transfer' with the details. "
                "   - If successful, inform 'Transfer successful!' and call 'signal_flutter_transfer_success' "
                "   - If error, say 'Transfer couldn\'t be completed. Would you like to try again?' "
                
                "## General Guidelines:"
                "- Keep responses short and clear "
                "- Combine questions when possible "
                "- Use defaults to speed up the process "
                "- Only ask for additional details if the user wants to provide them "
                "- Handle errors gracefully with simple explanations "
                "- For scheduled transfers, ensure the datetime is in UTC ISO format "
                "- Always confirm the schedule timing with the user before proceeding "
            ),
            tools=[get_temperature, set_temperature, get_similar_recipients, make_transfer, signal_flutter_transfer_success],
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
    await session.say("Hey, how can I help you with your banking today?", allow_interruptions=True)

if __name__ == "__main__":
    # Removed explicit multiprocessing.set_start_method call
    # livekit-agents should handle this internally.
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, port=8080))
