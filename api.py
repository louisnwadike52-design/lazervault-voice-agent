import enum
from typing import Annotated
from livekit.agents import function_tool, llm, RunContext
import logging

logger = logging.getLogger("temperature-control")
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
