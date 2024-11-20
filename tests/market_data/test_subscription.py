import logging
import time
from unittest import TestCase

from tastytrade_sdk import Subscription
from tastytrade_sdk.exceptions import InvalidArgument
from tastytrade_sdk.market_data.streamer_symbol_translation import StreamerSymbolTranslations
from tests.utils import get_tasty

TIMEOUT=30


class SubscriptionTest(TestCase):
    def test_requires_at_least_one_event_handler(self):
        with self.assertRaises(InvalidArgument):
            Subscription('url', 'token', StreamerSymbolTranslations([]))

    def test_subscription(self):
        tasty = get_tasty()
        symbols = ['AAPL']
        quotes = []
        fields = {'Quote': ['eventSymbol', 'askPrice']}

        subscription = tasty.market_data.subscribe(
            symbols=symbols,
            on_quote=lambda e: quotes.append(e),
            event_fields=fields)
        
        start = time.monotonic()
        subscription.open()
        self.addCleanup(subscription.close)
        time.sleep(1.0)
        while not (quotes or symbols or greeks):
            now = time.monotonic()
            if now - start > TIMEOUT:
                subscription.close()
                self.fail(f'Test timeout waiting for event data.\nEvents: quotes={len(quotes)}, candles={len(candles)}, greeks={len(greeks)}')
            time.sleep(1.0)

        # Check fields
        for quote in quotes:
            self.assertEqual(set(quote.keys()), {'eventSymbol', 'symbol', 'askPrice'})
