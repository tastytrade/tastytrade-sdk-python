from injector import inject

from tastytrade_sdk.api import Api
from tastytrade_sdk.orders.models import Order


class Orders:
    @inject
    def __init__(self, api: Api):
        self.__api = api

    def place_order(self, account_number: str, order: Order) -> dict:
        """
        https://developer.tastytrade.com/open-api-spec/orders/#/orders/postAccountsAccountNumberOrders
        """
        return self.__api.post(f'/accounts/{account_number}/orders', data=order.json)
