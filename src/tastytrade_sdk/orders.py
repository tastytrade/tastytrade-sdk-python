from dataclasses import dataclass
from typing import List

from injector import inject

from tastytrade_sdk import Api


@dataclass
class Leg:
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


class Orders:
    @inject
    def __init__(self, api: Api):
        self.__api = api

    def place_order(self, account_number: str, order: Order) -> dict:
        """
        https://developer.tastytrade.com/open-api-spec/orders/#/orders/postAccountsAccountNumberOrders
        """
        return self.__api.post(f'/accounts/{account_number}/orders', data=order.json)
