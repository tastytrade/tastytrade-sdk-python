from injector import Injector

from tastytrade_sdk.api import Api, RequestsSession
from tastytrade_sdk.market_data.market_data import MarketData


class Tastytrade:
    """
    The SDK's top-level class
    """

    def __init__(self):
        self.__container = Injector()

    def login(self, login: str, password: str) -> 'Tastytrade':
        """
        Initialize a logged-in session
        """
        self.__container.get(RequestsSession).login(login, password)
        return self

    def logout(self) -> None:
        """
        End the session
        """
        self.api.delete('/sessions')

    @property
    def market_data(self) -> MarketData:
        """
        Access the MarketData submodule
        """
        return self.__container.get(MarketData)

    @property
    def api(self) -> Api:
        """
        Access the Api submodule
        """
        return self.__container.get(Api)
