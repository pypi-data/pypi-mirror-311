from aiohttp import ClientConnectionError, ClientSession

from ._credit import credit, deposit, withdraw
from ._info import get_info
from ._orders import (
    cancel_order,
    create_order,
    fill_order,
    get_all_orders,
    get_order,
    get_orders,
)


async def status(
    session: ClientSession,
) -> bool:
    try:
        response = await session.get("/status")
        return response.ok
    except ClientConnectionError:
        return False


__all__ = [
    status,
    credit,
    deposit,
    withdraw,
    get_info,
    cancel_order,
    create_order,
    fill_order,
    get_all_orders,
    get_orders,
    get_order,
]
