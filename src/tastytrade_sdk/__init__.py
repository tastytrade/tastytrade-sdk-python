from injector import Injector

from tastytrade_sdk.api import Api
from tastytrade_sdk.instruments import Instruments
from tastytrade_sdk.market_metrics import MarketMetrics
from tastytrade_sdk.watchlists import Watchlists


class Tastytrade:
    def __init__(self):
        self.__injector = Injector()

    def login(self, login: str, password: str):
        """
        Login to tastytrade

        Parameters:
            login: The username or email you use to log in to tastytrade
            password: Your password
        """
        self.__injector.get(Api).login(login, password)

    @property
    def instruments(self) -> Instruments:
        """
        Returns:
            The Instruments service
        """
        return self.__injector.get(Instruments)

    @property
    def market_metrics(self) -> MarketMetrics:
        """
        Returns:
            The MarketMetrics service
        """
        return self.__injector.get(MarketMetrics)

    @property
    def watchlists(self) -> Watchlists:
        """
        Returns:
            The Watchlists service
        """
        return self.__injector.get(Watchlists)


__all__ = ['Tastytrade']
