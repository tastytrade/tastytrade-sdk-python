from injector import Injector

from tastytrade_sdk.api import Api, RequestsSession
from tastytrade_sdk.market_data.market_data import MarketData


class Tastytrade:
    def __init__(self):
        self.__container = Injector()

    def login(self, login: str, password: str) -> 'Tastytrade':
        self.__container.get(RequestsSession).login(login, password)
        return self

    def logout(self) -> None:
        self.api.delete('/sessions')

    @property
    def market_data(self) -> MarketData:
        return self.__container.get(MarketData)

    @property
    def api(self) -> Api:
        return self.__container.get(Api)
