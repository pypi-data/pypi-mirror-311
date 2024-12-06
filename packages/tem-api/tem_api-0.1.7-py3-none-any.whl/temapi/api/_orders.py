from typing import List, Optional

from aiohttp import ClientSession
from pydantic import TypeAdapter

from temapi.api._utils import build_url
from temapi.models import (
    CancelOrder,
    FillOrder,
    NewOrder,
    NewOrderId,
    Order,
    OrdersList,
    OrderStatus,
)


async def get_orders(
    session: ClientSession,
    *,
    skip: int = 0,
    take: int = 10,
    status: Optional[OrderStatus] = None,
    address: Optional[str] = None,
) -> OrdersList:
    args = {
        "skip": skip,
        "limit": take,
    }
    if status is not None:
        args["status"] = status
    if address is not None:
        args["address"] = address

    response = await session.get(build_url("/order/list", args))
    response.raise_for_status()
    return await response.json(loads=TypeAdapter(OrdersList).validate_json)


async def get_all_orders(
    session: ClientSession,
    *,
    status: Optional[OrderStatus] = None,
    address: Optional[str] = None,
) -> List[Order]:
    orders = list()
    skip = 0
    take = 100

    while True:
        chunk = await get_orders(
            session=session, skip=skip, take=take, status=status, address=address
        )
        chunk = chunk.list
        orders.extend(chunk)
        if len(chunk) < take:
            break
        skip += take

    return orders


async def get_order(session: ClientSession, id: int) -> Order:
    args = {
        "id": id,
    }

    response = await session.get(build_url("/order/info", args))
    response.raise_for_status()
    return await response.json(loads=TypeAdapter(Order).validate_json)


async def create_order(session: ClientSession, payload: NewOrder) -> int:
    payload.bulk = not isinstance(payload.address, str)
    response = await session.post(
        "/order/new",
        json=payload.model_dump(mode="json"),
    )
    response.raise_for_status()
    data: NewOrderId = await response.json(loads=TypeAdapter(NewOrderId).validate_json)
    return data.order


async def fill_order(session: ClientSession, payload: FillOrder) -> None:
    response = await session.post("/order/fill", json=payload.model_dump(mode="json"))
    response.raise_for_status()


async def cancel_order(session: ClientSession, payload: CancelOrder) -> None:
    response = await session.post("/order/cancel", json=payload.model_dump(mode="json"))
    response.raise_for_status()


# async def reclaim_order(session: ClientSession, payload: CancelOrder):
#     await session.post("/order/reclaim", json=payload.model_dump(mode="json"))
