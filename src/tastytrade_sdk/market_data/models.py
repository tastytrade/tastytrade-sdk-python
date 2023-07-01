from abc import ABC
from dataclasses import dataclass
from math import isnan
from typing import Optional, Union

NullableFloatStr = Optional[Union[float, str]]


def _float(value: NullableFloatStr) -> Optional[float]:
    if isinstance(value, str):
        return float(value) if value.isnumeric() else None
    if value is None:
        return None
    return None if isnan(value) else value


@dataclass
class Side(ABC):
    price: Optional[float]
    size: Optional[float]
    exchange_code: Optional[str]

    def __init__(self, price: NullableFloatStr, size: NullableFloatStr, exchange_code: Optional[str]):
        self.price = _float(price)
        self.size = _float(size)
        self.exchange_code = exchange_code


class Bid(Side):
    pass


class Ask(Side):
    pass


@dataclass
class Quote:
    symbol: str
    bid: Bid
    ask: Ask


@dataclass
class Candle:
    symbol: str
    time: int
    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    close: Optional[float]

    def __init__(self, symbol: str, time: int, _open: NullableFloatStr, high: NullableFloatStr, low: NullableFloatStr,
                 close: NullableFloatStr):
        self.symbol = symbol
        self.time = time
        self.open = _float(_open)
        self.high = _float(high)
        self.low = _float(low)
        self.close = _float(close)
