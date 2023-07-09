from unittest import TestCase

from tastytrade_sdk.market_data.subscription import Subscription
from tastytrade_sdk.exceptions import InvalidArgument
from tastytrade_sdk.market_data.streamer_symbol_translation import StreamerSymbolTranslations


class SubscriptionTest(TestCase):
    def test_requires_at_least_one_event_handler(self):
        with self.assertRaises(InvalidArgument):
            Subscription('url', 'token', StreamerSymbolTranslations([]))
