from injector import Injector

from tastytrade_sdk.api import Api
from tastytrade_sdk.market_data.market_data import MarketData


class Tastytrade:
    def __init__(self):
        self.__container = Injector()
        self.__api = self.__container.get(Api)

    def login(self, login: str, password: str) -> 'Tastytrade':
        self.api.login(login, password)
        return self

    def logout(self) -> None:
        self.api.delete('/sessions')

    @property
    def market_data(self) -> MarketData:
        return self.__container.get(MarketData)

    @property
    def api(self) -> Api:
        return self.__api
