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
class Quote:
    symbol: str
    bid_price: Optional[float]
    bid_size: Optional[float]
    bid_exchange_code: Optional[str]
    ask_price: Optional[float]
    ask_size: Optional[float]
    ask_exchange_code: Optional[str]

    def __init__(self, symbol: str, bid_price: NullableFloatStr, bid_size: NullableFloatStr,
                 bid_exchange_code: Optional[str], ask_price: NullableFloatStr, ask_size: NullableFloatStr,
                 ask_exchange_code: Optional[str]):
        """@private"""
        self.symbol = symbol
        self.bid_price = _float(bid_price)
        self.bid_size = _float(bid_size)
        self.bid_exchange_code = bid_exchange_code
        self.ask_price = _float(ask_price)
        self.ask_size = _float(ask_size)
        self.ask_exchange_code = ask_exchange_code


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
        """@private"""
        self.symbol = symbol
        self.time = time
        self.open = _float(_open)
        self.high = _float(high)
        self.low = _float(low)
        self.close = _float(close)
