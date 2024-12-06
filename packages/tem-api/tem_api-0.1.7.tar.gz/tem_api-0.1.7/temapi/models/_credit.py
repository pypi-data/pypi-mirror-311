from typing import Optional

from pydantic import BaseModel, Field

from temapi.models._orders import SignedMS


class Credit(BaseModel):
    value: int = Field(...)


class Deposit(BaseModel):
    address: str = Field(...)
    signed_tx: str = Field(...)


class Withdraw(BaseModel):
    address: str = Field(...)
    signed_ms: SignedMS = Field(...)
    amount: Optional[int] = Field(...)
