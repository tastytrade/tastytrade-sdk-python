__all__ = []

from injector import Injector

from tastytrade_sdk.api import Api
from tastytrade_sdk.watchlists import Watchlists


class Tastytrade:
    def __init__(self):
        self.__injector = Injector()

    def login(self, login: str, password: str):
        self.__injector.get(Api).login(login, password)

    @property
    def watchlists(self) -> Watchlists:
        return self.__injector.get(Watchlists)
