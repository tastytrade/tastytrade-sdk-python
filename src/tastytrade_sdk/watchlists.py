from typing import List

from injector import inject

from src.tastytrade_sdk.api import Api


class Watchlists:
    @inject
    def __init__(self, api: Api):
        self.__api = api

    def update(self, name: str, symbols: List[str] = tuple()) -> None:
        self.__api.put(f'/watchlists/{name}', {
            'name': name,
            'watchlist-entries': [{'symbol': x} for x in symbols]
        })
