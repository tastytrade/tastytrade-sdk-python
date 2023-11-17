import urllib.parse
from typing import List, Optional, Tuple, Any, Dict

from bidict import bidict
from injector import inject

from tastytrade_sdk.api import Api


class StreamerSymbolTranslations:
    def __init__(self, translations: Dict[str, str]):
        self.__bidict = bidict(translations)

    def get_streamer_symbol(self, symbol: str) -> str:
        return self.__bidict.get(symbol)

    def get_original_symbol(self, streamer_symbol: str) -> str:
        return self.__bidict.inv[streamer_symbol]

    @property
    def streamer_symbols(self) -> List[str]:
        return list(self.__bidict.values())


class StreamerSymbolTranslationsFactory:
    @inject
    def __init__(self, api: Api):
        self.__api = api

    def create(self, symbols: List[str]) -> StreamerSymbolTranslations:
        return StreamerSymbolTranslations({
            **self.__get_symbol_translations('equities', symbols),
            **self.__get_symbol_translations('futures', symbols),
            **self.__get_symbol_translations('equity-options', symbols, [('with-expired', True)]),
            **self.__get_symbol_translations('future-options', symbols),
            **self.__get_symbol_translations('cryptocurrencies', symbols)
        })

    def __get_symbol_translations(self, path_key: str, symbols: Optional[List[str]] = None,
                                  extra_params: Optional[List[Tuple[str, Any]]] = None) -> Dict[str, str]:
        if not symbols:
            return {}
        items = self.__api.get(
            f'/instruments/{path_key}',
            params=[('symbol[]', urllib.parse.quote(x.upper())) for x in symbols or []] + (extra_params or [])
        ).get('data').get('items')
        return {x['symbol']: x['streamer-symbol'] for x in items if 'streamer-symbol' in x}
