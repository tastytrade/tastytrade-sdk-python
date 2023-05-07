from dataclasses import dataclass
from typing import Iterator, List

from injector import inject

from tastytrade_sdk.api import Api


@dataclass
class Equity:
    symbol: str


@dataclass
class CompactOptionChain:
    expiration_type: str
    symbols: List[str]


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

    def get_compact_option_chains(self, symbol) -> List[CompactOptionChain]:
        response = self.__api.get(f'/option-chains/{symbol}/compact')
        if not response:
            return []
        return [
            CompactOptionChain(
                expiration_type=x['expiration-type'],
                symbols=x['symbols']
            )
            for x in response['data']['items']
        ]

    def __get_page(self, path: str, page_offset: int) -> dict:
        return self.__api.get(path, [('page-offset', page_offset)])


@dataclass
class Equity:
    symbol: str
