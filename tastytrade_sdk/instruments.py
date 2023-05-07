from dataclasses import dataclass
from typing import Iterator

from injector import inject

from tastytrade_sdk.api import Api


@dataclass
class Equity:
    symbol: str


class Instruments:
    @inject
    def __init__(self, api: Api):
        self.__api = api

    def get_active_equities(self) -> Iterator[Equity]:
        path = '/instruments/equities/active'
        page_offset = 0
        result = self.__get_page(path, page_offset)
        while True:
            for item in result['data']['items']:
                yield Equity(symbol=item['symbol'])
            if not result['pagination']['current-item-count']:
                return
            page_offset += 1
            result = self.__get_page(path, page_offset)

    def __get_page(self, path: str, page_offset: int) -> dict:
        return self.__api.get(path, [('page-offset', page_offset)])


@dataclass
class Equity:
    symbol: str
