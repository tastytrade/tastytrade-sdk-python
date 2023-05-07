from injector import Injector

from tastytrade_sdk.api import Api
from tastytrade_sdk.instruments import Instruments
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
    def watchlists(self) -> Watchlists:
        return self.__injector.get(Watchlists)


__all__ = ['Tastytrade']
