from aiohttp import ClientSession
from pydantic import TypeAdapter

from temapi.api._utils import build_url
from temapi.models._credit import Credit, Deposit, Withdraw


async def credit(session: ClientSession, address: str) -> int:
    response = await session.get(build_url("/credit", {"address": address}))
    response.raise_for_status()
    data: Credit = await response.json(loads=TypeAdapter(Credit).validate_json)
    return data.value


async def deposit(session: ClientSession, payload: Deposit):
    response = await session.post(
        url="/credit/deposit",
        json=payload.model_dump(mode="json", exclude_none=True, exclude_unset=True),
    )
    response.raise_for_status()


async def withdraw(session: ClientSession, payload: Withdraw):
    response = await session.post(
        url="/credit/withdraw",
        json=payload.model_dump(mode="json", exclude_none=True, exclude_unset=True),
    )
    response.raise_for_status()
