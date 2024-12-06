from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from temapi.models._common import MarketType, OrderStatus, OrderType, Resource, SignedMS


class Order(BaseModel):
    id: int = Field(...)
    type: OrderType = Field(...)
    market: MarketType = Field(...)
    origin: str = Field(...)
    target: str = Field(...)
    price: int = Field(...)
    amount: int = Field(...)
    freeze: int = Field(...)
    frozen: int = Field(...)
    resource: Resource = Field(...)
    locked: bool = Field(...)
    duration: int = Field(...)
    payment: int = Field(...)
    partfill: bool = Field(...)
    extend: bool = Field(...)
    maxlock: int = Field(...)
    status: OrderStatus = Field(...)
    archive: bool = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)


class OrdersList(BaseModel):
    list: List[Order] = Field([])
    total: int = Field(...)


class NewOrder(BaseModel):
    market: MarketType = Field(...)
    """Market type"""
    address: str = Field(...)
    """Sender of TRX"""
    target: str = Field(...)
    """Rent target"""
    payment: int = Field(...)
    """Payment in sun"""
    resource: Resource = Field(...)
    """Rented resource"""
    duration: int = Field(...)
    """Rent duration"""
    price: int = Field(...)
    """Rent price"""
    partfill: bool = Field(...)
    """Allow particular order execution"""
    bulk: bool = Field(...)
    """Order is bulk"""
    api_key: Optional[str] = Field(None)
    """User API key"""
    signed_ms: Optional[SignedMS] = Field(None)
    """Sing order"""
    signed_tx: Optional[str] = Field(None)
    """Sing TRX transaction"""


class NewOrderId(BaseModel):
    order: int = Field(...)


class FillOrder(BaseModel):
    id: int = Field(...)
    origin_address: Optional[str] = Field(None)
    address: str = Field(None)
    signed_tx: Optional[str] = Field(None)
    """Sing TRX transaction"""


class CancelOrder(BaseModel):
    order: int = Field(...)
    address: str = Field(...)
    signed_ms: SignedMS = Field(...)


# class ReclimeOrder(BaseModel):
#    pass
