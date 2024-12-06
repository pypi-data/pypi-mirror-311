from aiohttp import ClientSession
from pydantic import TypeAdapter

from temapi.models._info import Info


async def get_info(
    session: ClientSession,
) -> Info:
    response = await session.get("/info")
    response.raise_for_status()
    return await response.json(loads=TypeAdapter(Info).validate_json)
