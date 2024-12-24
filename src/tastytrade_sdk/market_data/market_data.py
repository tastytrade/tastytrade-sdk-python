import logging
from typing import Callable, List, Optional

from injector import inject

from tastytrade_sdk.api import Api
from tastytrade_sdk.market_data.streamer_symbol_translation import StreamerSymbolTranslationsFactory
from tastytrade_sdk.market_data.subscription import Subscription

_LOGGER = logging.getLogger(__name__)


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
                  on_quote: Callable[[dict], None] = None,
                  aggregation_period: Optional[float] = None,
                  event_fields: Optional[dict[str, list[str]]] = None,
                  **kwargs,
                  ) -> Subscription:
        """
        Subscribe to live feed data
        :param symbols: Symbols to subscribe to. Can be across multiple instrument types.
        :param on_candle: Handler for candle events
        :param on_greeks: Handler for greeks events
        :param on_quote: Handler for quote events
        :param aggregation_period: Desired aggregation period of events (in seconds)
        :param event_fields: If provided, a dict mapping one or more event types to lists of event fields.
            The event types recognized are 'Quote', 'Greeks', and 'Candle'. If specified, the server will be
            asked to send only these fields in a compact format. Compact events will be translated to the same
            dictionary format as full events, though with missing keys.
            Example:
            ```
            {
                "Quote": ["eventType", "eventSymbol", "bidPrice", "askPrice", "bidSize", "askSize"]
            }
            ```
        """
        data = self.__api.get('/api-quote-tokens')['data']
        _LOGGER.debug('Subscribing to DXLink feed: %s', data['dxlink-url'])
        return Subscription(
            data['dxlink-url'],
            data['token'],
            self.__streamer_symbol_translations_factory.create(symbols),
            on_candle=on_candle,
            on_greeks=on_greeks,
            on_quote=on_quote,
            aggregation_period=aggregation_period,
            event_fields=event_fields,
            **kwargs
        )
