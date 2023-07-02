from typing import List, Callable, Optional

from injector import inject

from tastytrade_sdk.api import Api
from tastytrade_sdk.market_data.streamer_symbol_translation import StreamerSymbolTranslationsFactory
from tastytrade_sdk.market_data.subscription import Subscription
from tastytrade_sdk.market_data.models import Candle, Quote, Greeks


class MarketData:
    """
    Submodule for streaming market data
    """

    @inject
    def __init__(self, api: Api, streamer_symbol_translations_factory: StreamerSymbolTranslationsFactory):
        """@private"""
        self.__api = api
        self.__streamer_symbol_translations_factory = streamer_symbol_translations_factory

    def subscribe(self, symbols: List[str], on_quote: Optional[Callable[[Quote], None]] = None,
                  on_candle: Optional[Callable[[Candle], None]] = None,
                  on_greeks: Optional[Callable[[Greeks], None]] = None) -> Subscription:
        """
        Subscribe to live feed data
        :param symbols: Symbols to subscribe to. Can be across multiple instrument types.
        :param on_quote: Handler for `Quote` events
        :param on_candle: Handler for `Candle` events
        :param on_greeks: Handler for `Greeks` events
        """
        data = self.__api.get('/quote-streamer-tokens')['data']
        return Subscription(
            data['dxlink-url'],
            data['token'],
            self.__streamer_symbol_translations_factory.create(symbols),
            on_quote,
            on_candle,
            on_greeks
        )
