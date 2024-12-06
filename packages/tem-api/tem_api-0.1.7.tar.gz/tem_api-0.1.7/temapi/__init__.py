from temapi.api import (
    cancel_order,
    create_order,
    credit,
    deposit,
    fill_order,
    get_all_orders,
    get_info,
    get_order,
    get_orders,
    status,
    withdraw,
)
from temapi.models import (
    CancelOrder,
    FillOrder,
    Info,
    MarketType,
    NewOrder,
    NewOrderId,
    Order,
    OrdersList,
    OrderStatus,
    OrderType,
    Resource,
    SignedMS,
)

TEM_BASE_URL = "https://api.tronenergy.market/"


def payment(price: int, amount: int, duration: int) -> int:
    """
    Calculate the total payment for an order based on price, amount, and duration.

    Args:
        price (int): The price per unit of resource.
        amount (int): The amount of resource being ordered.
        duration (int): The duration for which the resource is being ordered.

    Returns:
        int: The total payment required for the order.
    """
    return int(
        (price * amount * (duration + (86400 if duration < 86400 else 0))) / 86400
    )


__all__ = [
    TEM_BASE_URL,
    Order,
    CancelOrder,
    FillOrder,
    MarketType,
    NewOrder,
    NewOrderId,
    OrderStatus,
    OrderType,
    SignedMS,
    Info,
    OrdersList,
    Resource,
    cancel_order,
    create_order,
    credit,
    deposit,
    fill_order,
    get_all_orders,
    get_info,
    get_order,
    get_orders,
    status,
    withdraw,
    payment,
]
