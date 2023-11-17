from typing import List, Callable

from injector import inject

from tastytrade_sdk.api import Api
from tastytrade_sdk.market_data.streamer_symbol_translation import StreamerSymbolTranslationsFactory
from tastytrade_sdk.market_data.subscription import Subscription


class MarketData:
    """
    Submodule for streaming market data
    """

    @inject
    def __init__(self, api: Api, streamer_symbol_translations_factory: StreamerSymbolTranslationsFactory):
        """@private"""
        self.__api = api
        self.__streamer_symbol_translations_factory = streamer_symbol_translations_factory

    def subscribe(self,
                  symbols: List[str],
                  on_candle: Callable[[dict], None] = None,
                  on_greeks: Callable[[dict], None] = None,
                  on_quote: Callable[[dict], None] = None
                  ) -> Subscription:
        """
        Subscribe to live feed data
        :param symbols: Symbols to subscribe to. Can be across multiple instrument types.
        :param on_candle: Handler for candle events
        :param on_greeks: Handler for greeks events
        :param on_quote: Handler for quote events
        """
        data = self.__api.get('/quote-streamer-tokens')['data']
        return Subscription(
            data['dxlink-url'],
            data['token'],
            self.__streamer_symbol_translations_factory.create(symbols),
            on_candle=on_candle,
            on_greeks=on_greeks,
            on_quote=on_quote
        )
