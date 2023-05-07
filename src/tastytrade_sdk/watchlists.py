from typing import List

from injector import inject

from tastytrade_sdk.api import Api


class Watchlists:
    """
    Watchlists
    """
    @inject
    def __init__(self, api: Api):
        self.__api = api

    def update(self, name: str, symbols: List[str] = tuple()) -> None:
        """
        Update a watchlist

        :param name:
        :param symbols:
        :return:
        """
        self.__api.put(f'/watchlists/{name}', {
            'name': name,
            'watchlist-entries': [{'symbol': x} for x in symbols]
        })
