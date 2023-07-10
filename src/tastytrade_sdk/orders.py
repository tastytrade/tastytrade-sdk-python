from dataclasses import dataclass
from typing import List, Optional

from injector import inject

from tastytrade_sdk.accounts.accounts import Accounts
from tastytrade_sdk.api import Api


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
    price: Optional[float] = None
    price_effect: Optional[str] = None

    @property
    def json(self) -> dict:
        return {
            'order-type': self.order_type,
            'time-in-force': self.time_in_force,
            'price': self.price,
            'price-effect': self.price_effect,
            'legs': [leg.json for leg in self.legs]
        }


class Orders:
    @inject
    def __init__(self, api: Api, accounts: Accounts):
        self.__api = api
        self.__accounts = accounts

    def place_order(self, account_number: str, order: Order) -> dict:
        """
        https://developer.tastytrade.com/open-api-spec/orders/#/orders/postAccountsAccountNumberOrders
        """
        return self.__api.post(f'/accounts/{account_number}/orders', data=order.json)

    def place_order_and_wait(self, account_number: str, order: Order, timeout_seconds: Optional[int] = None) -> bool:
        """
        Place an order and wait for all legs to get filled
        :param account_number: Account number
        :param order: Order to place
        :param timeout_seconds: How long to wait for fills. If not provided, will wait indefinitely
        :return: True if all legs were filled, False if timed out
        """
        order_id = self.__api.post(f'/accounts/{account_number}/orders', data=order.json)['data']['order']['id']
        streamer = self.__accounts.get_streamer(account_numbers=[account_number])

        is_all_filled = False

        def __is_all_filled(_order: dict) -> bool:
            return all(leg['remaining-quantity'] == 0 for leg in _order['legs'])

        def __on_message(message: dict) -> None:
            nonlocal is_all_filled
            if message.get('type') == 'Order' and message['data']['id'] == order_id:
                if __is_all_filled(message['data']):
                    is_all_filled = True
                    streamer.stop()

        streamer.start(on_message=__on_message, timeout_seconds=timeout_seconds)

        if __is_all_filled(self.__api.get(f'/accounts/{account_number}/orders/{order_id}')['data']):
            is_all_filled = True
            streamer.stop()

        streamer.join()
        return is_all_filled

    def cancel(self, account_number: str, order_ids: List[int]) -> None:
        """
        https://developer.tastytrade.com/open-api-spec/orders/#/orders/deleteAccountsAccountNumberOrdersId
        """
        for order_id in order_ids:
            self.__api.delete(f'/accounts/{account_number}/orders/{order_id}')
