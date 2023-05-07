from typing import Optional

from injector import Injector

from tastytrade_sdk.api import Api
from tastytrade_sdk.instruments import Instruments
from tastytrade_sdk.market_metrics import MarketMetrics
from tastytrade_sdk.watchlists import Watchlists

"""
Tastytrade
====================================
Testing
"""


class Tastytrade:
    def __init__(self, login: Optional[str] = None, password: Optional[str] = None):
        self.__injector = Injector()
        if login and password:
            self.login(login, password)

    def login(self, login: str, password: str):
        """
        Login to tastytrade
        Parameters
        ----------
        login
            The username or email you use to log in to tastytrade
        password
            Your tastytrade password
        """
        self.__injector.get(Api).login(login, password)

    @property
    def instruments(self) -> Instruments:
        return self.__injector.get(Instruments)

    @property
    def market_metrics(self) -> MarketMetrics:
        return self.__injector.get(MarketMetrics)

    @property
    def watchlists(self) -> Watchlists:
        return self.__injector.get(Watchlists)


__all__ = ['Tastytrade']
