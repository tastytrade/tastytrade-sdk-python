import logging
from itertools import product
from math import floor
from typing import Callable, Optional

from tastytrade_sdk.exceptions import TastytradeSdkException
from tastytrade_sdk.websocket import Websocket
from tastytrade_sdk.market_data.streamer_symbol_translation import StreamerSymbolTranslations


class Subscription:
    __is_authorized: bool = False

    def __init__(self, url: str, token: str, streamer_symbol_translations: StreamerSymbolTranslations,
                 on_message: Callable[[dict], None] = logging.info):
        """@private"""
        self.__token = token
        self.__streamer_symbol_translations = streamer_symbol_translations
        self.__on_message = on_message
        self.__websocket = Websocket(url)

    def open(self) -> 'Subscription':
        """Start listening for feed events"""
        self.__websocket.open(connect_action=lambda: self.__send('SETUP', version='0.1-js/1.0.0'),
                              on_message=self.__wrap_on_message(),
                              keepalive_action=lambda: self.__send('KEEPALIVE'))
        subscription_types = ['Quote', 'Candle', 'Greeks']
        subscriptions = [{'symbol': s, 'type': t} for s, t in
                         product(self.__streamer_symbol_translations.streamer_symbols, subscription_types)]
        self.__send('AUTH', token=self.__token)
        while not self.__is_authorized:
            continue
        self.__send('CHANNEL_REQUEST', channel=1, service='FEED', parameters={'contract': 'AUTO'})
        self.__send('FEED_SUBSCRIPTION', channel=1, add=subscriptions)
        return self

    def close(self) -> None:
        """Close the stream connection"""
        if self.__websocket:
            self.__websocket.close()

    def __wrap_on_message(self) -> Callable[[dict], None]:
        def __on_message(message: Optional[dict]) -> None:
            if not message:
                return
            _type = message['type']
            if _type == 'ERROR':
                raise StreamerException(message['error'], message['message'])
            if _type == 'SETUP':
                keepalive_interval = floor(message['keepaliveTimeout'] / 2)
                self.__websocket.update_keepalive_timeout_seconds(keepalive_interval)
            elif _type == 'AUTH_STATE':
                self.__is_authorized = message['state'] == 'AUTHORIZED'
            elif _type == 'FEED_DATA':
                for event in message['data']:
                    event['symbol'] = self.__streamer_symbol_translations.get_original_symbol(event['eventSymbol'])
                    self.__on_message(event)
            else:
                logging.debug('Unhandled message type: %s', _type)

        return __on_message

    def __send(self, _type: str, channel: Optional[int] = 0, **kwargs) -> None:
        self.__websocket.send({
            **{'type': _type, 'channel': channel},
            **kwargs
        })


class StreamerException(TastytradeSdkException):
    def __init__(self, error: str, message: str):
        super().__init__(f'{error}: {message}')
