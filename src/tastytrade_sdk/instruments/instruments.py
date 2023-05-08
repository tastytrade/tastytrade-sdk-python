from types import MappingProxyType
from typing import Iterator, List, Optional, Any, Dict, Callable, TypeVar

from injector import inject

from tastytrade_sdk.api import Api
from tastytrade_sdk.instruments.models import Lendability, Equity, CompactOptionChain

T = TypeVar('T')


class Instruments:
    @inject
    def __init__(self, api: Api):
        self.__api = api

    def get_active_equities(self, lendability: Optional[Lendability] = None) -> Iterator[Equity]:
        params = {}
        if lendability:
            params['lendability'] = lendability.value
        return self.__get_paginated('/instruments/equities/active', lambda x: Equity(x['symbol']), params)

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

    def __get_paginated(self, path: str, item_handler: Callable[[dict], T],
                        params: Dict[str, Any] = MappingProxyType({})) -> Iterator[T]:

        params_as_tuples = [(k, v) for k, v in params.items()]

        def __get_page(_page_offset: int) -> dict:
            return self.__api.get(path, params_as_tuples + [('page-offset', page_offset)])

        page_offset = 0
        result = __get_page(page_offset)
        while True:
            for item in result['data']['items']:
                yield item_handler(item)
            if not result['pagination']['current-item-count']:
                return
            page_offset += 1
            result = __get_page(page_offset)
