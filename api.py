import enum
from typing import Annotated, List, Dict, Any
from livekit.agents import function_tool, llm, RunContext, JobContext
import logging
import aiohttp
import json
import os
from datetime import datetime

# Use __name__ for logger consistency
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Zone(enum.Enum):
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    OFFICE = "office"


# Global state for temperatures (simplification for now)
_temperature_state = {
    Zone.LIVING_ROOM: 22,
    Zone.BEDROOM: 20,
    Zone.KITCHEN: 24,
    Zone.BATHROOM: 23,
    Zone.OFFICE: 21,
}


@function_tool(description="Get the temperature in a specific room. Valid zones are living_room, bedroom, kitchen, bathroom, office.")
async def get_temperature(
    context: RunContext,
    zone: Zone
) -> str:
    try:
        zone_enum = Zone(str(zone))
    except ValueError:
        if isinstance(zone, Zone):
            zone_enum = zone
        else:
            logger.warning(f"Unknown zone value received: {zone} of type {type(zone)}")
            return f"Unknown zone: {zone}. Please specify a valid zone."
    
    logger.info("get_temperature - zone %s", zone_enum.value)
    temp = _temperature_state[zone_enum]
    return f"The temperature in the {zone_enum.value} is {temp}C"


@function_tool(description="Set the temperature in a specific room. Valid zones are living_room, bedroom, kitchen, bathroom, office.")
async def set_temperature(
    context: RunContext,
    zone: Zone,
    temp: int,
) -> str:
    try:
        zone_enum = Zone(str(zone))
    except ValueError:
        if isinstance(zone, Zone):
            zone_enum = zone
        else:
            logger.warning(f"Unknown zone value received: {zone} of type {type(zone)}")
            return f"Unknown zone: {zone}. Please specify a valid zone."

    logger.info("set_temperature - zone %s, temp: %s", zone_enum.value, temp)
    _temperature_state[zone_enum] = temp
    return f"The temperature in the {zone_enum.value} is now {temp}C"

# New banking functions

# Use the BASE_API_URL from the environment, with a fallback just in case.
# The /v1 suffix will be added to this base.
BASE_API_URL_ROOT = os.getenv('BASE_API_URL', 'https://lazervault-golang-http-805149139138.europe-west1.run.app')
BASE_API_URL = f"{BASE_API_URL_ROOT}/v1" # Add /v1 prefix

@function_tool(description="Get a list of similar recipients by name to transfer money to. Helps identify the correct recipient if unsure.")
async def get_similar_recipients(
    context: RunContext,
    name: Annotated[str, "The first name or full name of the recipient to search for."]
) -> str:
    logger.info(f"get_similar_recipients - name: {name}")
    url = f"{BASE_API_URL}/recipients/search-by-name" 
    params = {'name': name}
    logger.info(f"get_similar_recipients - url: {url}, params: {params}")
    headers = {}
    
    # Get token from userdata
    access_token = context.userdata.get("access_token") 
    
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
        logger.info("Access token found in userdata, adding Authorization header for get_similar_recipients.")
    else:
        logger.warning("Access token not found in RunContext userdata for get_similar_recipients. Call might fail if auth is required.")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                response_text = await response.text()
                logger.info(f"Response from get-similar-recipients: {response.status} - {response_text}")
                if response.status == 200:
                    try:
                        # Attempt to parse to validate JSON, but return the original string
                        json.loads(response_text)
                        return response_text
                    except json.JSONDecodeError:
                        logger.error("Failed to decode JSON from get_similar_recipients")
                        return "Error: Received invalid data format from the recipients service."
                else:
                    # Propagate API error details if possible
                    return f"Error: Could not fetch recipients. Status: {response.status} - {response_text}"
    except aiohttp.ClientConnectorError as e:
        logger.error(f"Connection error in get_similar_recipients: {e}")
        return f"Error: Could not connect to the recipients service. {e}"
    except Exception as e:
        logger.error(f"Unexpected error in get_similar_recipients: {e}")
        return f"Error: An unexpected error occurred while fetching recipients. {e}"

@function_tool(description="Transfers money to a specified recipient after gathering all necessary details and user authorization.")
async def make_transfer(
    context: RunContext,
    amount: Annotated[str, "The amount of money to transfer."],
    recipient_id: Annotated[str, "The unique ID of the recipient."],
    description: Annotated[str, "A short description or memo for the transfer."] = "",
    category: Annotated[str, "The category of the transfer (e.g., Shopping, Utilities, Rent)."] = "",
    reference: Annotated[str, "A reference for the transfer."] = "",
    from_account_id: Annotated[str, "The account ID from which the money is being sent. Default is '1'."] = "1",
    to_account_id: Annotated[str, "The account ID to which the money is being sent (used if recipient_id is not valid or available)."] = None,
    scheduled_at: Annotated[str, "The scheduled date and time for the transfer in ISO format. Empty string for immediate transfer."] = ""
) -> str:
    logger.info(f"make_transfer called with - amount: {amount}, recipient_id arg: '{recipient_id}', to_account_id arg: '{to_account_id}', from_account_id: {from_account_id}, scheduled_at: {scheduled_at}")

    # Validate scheduled_at format if provided
    if scheduled_at and scheduled_at.strip():
        try:
            # Try to parse the ISO format string to validate it
            datetime.fromisoformat(scheduled_at.replace('Z', '+00:00'))
        except ValueError:
            logger.error(f"Invalid scheduled_at format: {scheduled_at}")
            return "Error: Invalid scheduled date format. Please provide a valid ISO format datetime string."

    # Build base payload with defaults
    payload = {
        "amount": amount,
        "category": category if category else "Miscellaneous",
        "description": description if description else f"Transfer payment to {recipient_id}",
        "from_account_id": from_account_id,
        "reference": reference if reference else "default",
        "scheduled_at": scheduled_at.strip() if scheduled_at else ""
    }

    valid_recipient_id_str = recipient_id.strip() if recipient_id else None
    valid_to_account_id_str = to_account_id.strip() if to_account_id else None

    if valid_recipient_id_str:
        payload["recipient_id"] = valid_recipient_id_str
        logger.info(f"Using recipient_id: {valid_recipient_id_str} for the transfer.")
    elif valid_to_account_id_str:
        payload["to_account_id"] = valid_to_account_id_str
        logger.info(f"Using to_account_id: {valid_to_account_id_str} as recipient_id was not valid.")
    else:
        logger.error("make_transfer: Neither recipient_id nor to_account_id provided a valid identifier.")
        return "Error: A valid recipient identifier (recipient_id or to_account_id) is required for the transfer."

    url = f"{BASE_API_URL}/transfers" 
    logger.info(f"Sending transfer request to {url} with payload: {json.dumps(payload)}")

    headers = {}
    # Get token from userdata
    access_token = context.userdata.get("access_token")
    
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
        logger.info("Access token found in userdata, adding Authorization header for make_transfer.")
    else:
        logger.warning("Access token not found in RunContext userdata for make_transfer. Call might fail if auth is required.")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                response_text = await response.text()
                logger.info(f"Response from make_transfer: {response.status} - {response_text}")
                if response.status == 200 or response.status == 201:
                    try:
                       json.loads(response_text)
                       return response_text
                    except json.JSONDecodeError:
                       logger.error("Failed to decode JSON response from make_transfer")
                       return "Error: Received invalid data format from the transfer service."
                else:
                    return f"Error: Transfer failed. Status: {response.status} - {response_text}"
    except aiohttp.ClientConnectorError as e:
        logger.error(f"Connection error in make_transfer: {e}")
        return f"Error: Could not connect to the transfer service. {e}"
    except Exception as e:
        logger.error(f"Unexpected error in make_transfer: {e}")
        return f"Error: An unexpected error occurred during the transfer. {e}"

@function_tool(description="Signals the frontend that a transfer was successful, providing the transaction details. This tool should ONLY be called by the AI after a successful 'make_transfer' call.")
async def signal_flutter_transfer_success(
    context: RunContext,
    transaction_response: Annotated[str, "The JSON string response received from the successful 'make_transfer' operation."]
) -> str:
    logger.info(f"Tool signal_flutter_transfer_success called with: {transaction_response}")
    try:
        # Access room directly from context
        room = context.room

        # Parse the JSON data
        parsed_data = json.loads(transaction_response) 
        
        payload_to_send = json.dumps({
            "event": "transfer_completed", 
            "data": parsed_data
        })

        await room.send_data(
            payload=payload_to_send,
            topic="flutter_updates"
        )
        logger.info(f"Successfully sent transfer_completed signal via tool. Payload: {payload_to_send}")
        # Return a success message to the LLM
        return "Frontend signal sent successfully."

    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON in signal_flutter_transfer_success tool: {e}")
        return f"Error: Invalid transaction data format: {e}"
    except AttributeError as e:
         logger.error(f"Error accessing room object in signal_flutter_transfer_success: {e}")
         return "Error: Could not access room to send signal."
    except Exception as e:
        logger.error(f"Unexpected error in signal_flutter_transfer_success tool: {e}")
        return f"Error: An unexpected error occurred while sending signal: {e}"
