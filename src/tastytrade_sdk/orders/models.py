from dataclasses import dataclass
from typing import List


@dataclass
class Leg:
    """@private"""
    instrument_type: str
    symbol: str
    action: str
    quantity: float

    @property
    def json(self) -> dict:
        return {
            'instrument-type': self.instrument_type,
            'symbol': self.symbol,
            'action': self.action,
            'quantity': self.quantity
        }


@dataclass
class Order:
    """@private"""
    order_type: str
    time_in_force: str
    legs: List[Leg]

    @property
    def json(self) -> dict:
        return {
            'order-type': self.order_type,
            'time-in-force': self.time_in_force,
            'legs': [leg.json for leg in self.legs]
        }
