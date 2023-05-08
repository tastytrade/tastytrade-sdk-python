from typing import Optional

from injector import Injector

from tastytrade_sdk.api import Api
from tastytrade_sdk.instruments import Instruments
from tastytrade_sdk.market_metrics import MarketMetrics
from tastytrade_sdk.watchlists import Watchlists


class Tastytrade:
    def __init__(self):
        self.__injector = Injector()

    def login(self, login: str, password: str):
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

