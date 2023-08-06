from typing import TypedDict


class TradingFee(TypedDict):
    symbol: str
    actualMakerRate: str
    actualTakerRate: str
    takerFeeRate: str
    makerFeeRate: str


class FeeRateResponse(TypedDict):
    status: str
    data: list[TradingFee]
