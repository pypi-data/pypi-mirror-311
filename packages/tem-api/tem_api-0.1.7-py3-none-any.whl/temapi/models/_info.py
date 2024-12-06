from typing import List

from pydantic import BaseModel, Field


class AvailableByPriceInfo(BaseModel):
    price: int = Field(...)
    value: float = Field(...)


class MarketInfo(BaseModel):
    availableEnergy: float = Field(...)
    availableFastEnergy: float = Field(...)
    availableEnergyByPrice: List[AvailableByPriceInfo] = Field([])
    totalEnergy: int = Field(...)
    nextReleaseEnergy: int = Field(...)
    availableBandwidth: float = Field(...)
    availableFastBandwidth: float = Field(...)
    availableBandwidthByPrice: List[AvailableByPriceInfo] = Field([])
    totalBandwidth: int = Field(...)
    nextReleaseBandwidth: int = Field(...)
    energyPerTrxFrozen: float = Field(...)
    bandwidthPerTrxFrozen: float = Field(...)
    trxPerEnergyFee: float = Field(...)
    trxPerBandwidthFee: float = Field(...)


class PriceInfoItem(BaseModel):
    minDuration: int = Field(...)
    basePrice: int = Field(...)
    minPoolPrice: int = Field(...)
    suggestedPrice: int = Field(...)


class PriceInfo(BaseModel):
    openEnergy: List[PriceInfoItem] = Field([])
    fastEnergy: List[PriceInfoItem] = Field([])
    openBandwidth: List[PriceInfoItem] = Field([])
    fastBandwidth: List[PriceInfoItem] = Field([])


class OrderInfo(BaseModel):
    minEnergy: int = Field(...)
    suggestedEnergy: int = Field(...)
    minBandwidth: int = Field(...)
    suggestedBandwidth: int = Field(...)
    minFillEnergy: int = Field(...)
    minFillBandwidth: int = Field(...)
    openDurations: List[int] = Field([])
    openSuggestedDuration: int = Field(...)
    fastDurations: List[int] = Field([])
    fastSuggestedDuration: int = Field(...)
    publicTime: int = Field(...)
    fillOrderAward: float = Field(...)
    cancellationFee: int = Field(...)


class PoolInfo(BaseModel):
    pass


class CreditInfo(BaseModel):
    minAmount: int = Field(...)
    minTimeToWithdraw: int = Field(...)


class ReferralInfo(BaseModel):
    reward: float = Field(...)


class RewardInfo(BaseModel):
    tokenId: str = Field(...)
    exchangeId: int = Field(...)
    exchangeTokenAmount: int = Field(...)
    exchangeTrxAmount: int = Field(...)


class TronInfo(BaseModel):
    node: str = Field(...)
    tronscan: str = Field(...)
    tronscanApi: str = Field(...)


class Info(BaseModel):
    address: str = Field(...)
    market: MarketInfo = Field(...)
    price: PriceInfo = Field(...)
    order: OrderInfo = Field(...)
    pool: PoolInfo = Field(...)
    credit: CreditInfo = Field(...)
    referral: ReferralInfo = Field(...)
    reward: RewardInfo = Field(...)
    tron: TronInfo = Field(...)
