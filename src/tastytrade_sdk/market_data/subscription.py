# pylint: disable=c-extension-no-member
import logging
import threading
import time
from itertools import product
from math import floor
from typing import Callable, Optional

import ujson
from websockets.exceptions import ConnectionClosedOK
from websockets.sync.client import connect, ClientConnection

from tastytrade_sdk.exceptions import TastytradeSdkException, InvalidArgument
from tastytrade_sdk.market_data.streamer_symbol_translation import StreamerSymbolTranslations

_LOGGER = logging.getLogger(__name__)


class LoopThread(threading.Thread):
    def __init__(self, activity: Callable, timeout_seconds: int = 0):
        threading.Thread.__init__(self)
        self.__running = True
        self.__activity = activity
        self.__timeout_seconds = timeout_seconds
        self.__condition = threading.Condition()
        super().start()

    def run(self):
        while self.__running:
            self.__activity()
            self.__pause()

    def __pause(self):
        if not self.__timeout_seconds:
            return
        start = time.monotonic()
        cond = self.__condition
        remaining = self.__timeout_seconds
        while self.__running and remaining > 0:
            now = time.monotonic()
            remaining = self.__timeout_seconds - (now - start)
            if remaining > 0:
                with cond:
                    cond.wait(remaining)

    def stop(self):
        with self.__condition:
            self.__running = False
            self.__condition.notify()


class Subscription:
    __websocket: Optional[ClientConnection] = None
    __keepalive_thread: Optional[LoopThread]
    __receive_thread: Optional[LoopThread]
    __is_authorized: bool = False
    __channel_opened: Optional[dict] = None
    __feed_config: Optional[dict] = None
    __aggregation_period: Optional[float] = None
    __event_fields: Optional[dict[str, list[str]]] = None
    __condition: threading.Condition

    def __init__(self, url: str, token: str, streamer_symbol_translations: StreamerSymbolTranslations,
                 on_candle: Callable[[dict], None] = None,
                 on_greeks: Callable[[dict], None] = None,
                 on_quote: Callable[[dict], None] = None,
                 aggregation_period: Optional[float] = None,
                 event_fields: Optional[dict[str, list[str]]] = None,
                 ):
        """@private"""

        if not (on_quote or on_candle or on_greeks):
            raise InvalidArgument('At least one feed event handler must be provided')

        self.__condition = threading.Condition()
        self.__url = url
        self.__token = token
        self.__streamer_symbol_translations = streamer_symbol_translations
        self.__on_quote = on_quote
        self.__on_candle = on_candle
        self.__on_greeks = on_greeks
        self.__aggregation_period = aggregation_period
        self.__event_fields = event_fields

    def open(self) -> 'Subscription':
        """Start listening for feed events"""
        self.__websocket = connect(self.__url)
        self.__receive_thread = LoopThread(self.__receive)

        subscription_types = []
        if self.__on_quote:
            subscription_types.append('Quote')
        if self.__on_candle:
            subscription_types.append('Candle')
        if self.__on_greeks:
            subscription_types.append('Greeks')

        subscriptions = [{'symbol': s, 'type': t} for s, t in
                         product(self.__streamer_symbol_translations.streamer_symbols, subscription_types)]

        self.__send('SETUP', version='0.1-js/1.0.0')
        self.__send('AUTH', token=self.__token)
        self.__wait_for(lambda: self.__is_authorized)

        self.__channel_opened = None
        self.__send('CHANNEL_REQUEST', channel=1, service='FEED', parameters={'contract': 'AUTO'})
        self.__wait_for(lambda: self.__channel_opened)

        self.__feed_config = None

        setup_params = {}
        if self.__aggregation_period is not None:
            setup_params['acceptAggregationPeriod'] = self.__aggregation_period
        if self.__event_fields:
            setup_params['acceptDataFormat'] = 'COMPACT'
            setup_params['acceptEventFields'] = self.__event_fields
        else:
            setup_params['acceptDataFormat'] = 'FULL'
        self.__send('FEED_SETUP', channel=1, **setup_params)

        self.__send('FEED_SUBSCRIPTION', channel=1, add=subscriptions)
        return self

    def close(self) -> None:
        """Close the stream connection"""
        if thread := self.__keepalive_thread:
            thread.stop()
            thread.join()
            self.__keepalive_thread = None
        if thread := self.__receive_thread:
            thread.stop()
            thread.join()
            self.__receive_thread = None
        if socket := self.__websocket:
            socket.close()
            self.__websocket = None
        self.__feed_config = None
        self.__is_authorized = False
        self.__channel_opened = None

    def __wait_for(self, condition: Callable):
        with self.__condition:
            self.__condition.wait_for(condition, 0.1)

    # pylint: disable=too-many-branches
    def __receive(self) -> None:
        if not self.__websocket:
            return
        try:
            message = ujson.loads(self.__websocket.recv())
        except ConnectionClosedOK:
            return
        _type = message['type']
        cond = self.__condition
        # TODO: Convert this into some more appropriate structure to avoid branch bloat.
        if _type == 'ERROR':
            raise StreamerException(message['error'], message['message'])
        if _type == 'SETUP':
            keepalive_interval = floor(message['keepaliveTimeout'] / 2)
            self.__keepalive_thread = LoopThread(lambda: self.__send('KEEPALIVE'), keepalive_interval)
        elif _type == 'AUTH_STATE':
            auth_state = message['state'] == 'AUTHORIZED'
            with cond:
                self.__is_authorized = auth_state
                cond.notify_all()
            _LOGGER.debug('Got auth state: %s', auth_state)
        elif _type == 'FEED_CONFIG':
            with cond:
                self.__feed_config = message
                cond.notify_all()
            _LOGGER.info('Got feed config: %s', message)
        elif _type == 'CHANNEL_OPENED':
            with cond:
                self.__channel_opened = message
                cond.notify_all()
            _LOGGER.info('Got channel open: %s', message)
        elif _type == 'KEEPALIVE':
            pass
        elif _type == 'FEED_DATA':
            data = message['data']
            event_type = None
            event_handler: Optional[Callable] = None
            for event in data:
                if isinstance(event, str):
                    event_type = event
                    event_handler = self.__handler_for(event_type)
                elif isinstance(event, list):
                    if event_handler:
                        full_event = self.__unpack_event(event_type, event)
                        event_handler(full_event)  # pylint: disable=not-callable
                elif isinstance(event, dict):
                    handler = self.__handler_for(event['eventType'])
                    if handler:
                        self.__update_event(event)
                        handler(event)
        else:
            _LOGGER.debug('Unhandled message type: %s', _type)
    # pyline: enable=too-many-branches

    def __unpack_event(self, event_type, event) -> Optional[list[str]]:
        if (config := self.__feed_config) and (config_fields := config.get('eventFields')):
            fields = config_fields.get(event_type)
            if len(event) != len(fields):
                raise ValueError(f'Event and field length do not match: {len(event)} vs {len(fields)}')
            full_event = dict(zip(fields, event))
            self.__update_event(full_event)
            return full_event
        return None

    def __update_event(self, event: dict) -> None:
        if symbol := event.get('eventSymbol'):
            original_symbol = self.__streamer_symbol_translations.get_original_symbol(symbol)
            event['symbol'] = original_symbol

    def __handler_for(self, event_type) -> Optional[Callable]:
        if event_type == 'Quote' and self.__on_quote:
            return self.__on_quote
        if event_type == 'Candle' and self.__on_candle:
            return self.__on_candle
        if event_type == 'Greeks' and self.__on_greeks:
            return self.__on_greeks
        _LOGGER.debug('No handler registered for %s', event_type)
        return None

    def __send(self, _type: str, channel: Optional[int] = 0, **kwargs) -> None:
        self.__websocket.send(ujson.dumps({
            **{'type': _type, 'channel': channel},
            **kwargs
        }))


class StreamerException(TastytradeSdkException):
    def __init__(self, error: str, message: str):
        super().__init__(f'{error}: {message}')
