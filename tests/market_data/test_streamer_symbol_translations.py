from unittest import TestCase, skip

from tastytrade_sdk.market_data.streamer_symbol_translation import StreamerSymbolTranslationsFactory
from tastytrade_sdk import Tastytrade


class StreamerSymbolTranslationsFactoryTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.__factory = StreamerSymbolTranslationsFactory(Tastytrade.from_env().api)

    def test_equities(self):
        translations = self.__factory.create(['SPY', 'AAPL', 'FOO'])
        self.assertIsNotNone(translations.get_streamer_symbol('SPY'))
        self.assertIsNotNone(translations.get_streamer_symbol('AAPL'))
        self.assertIsNone(translations.get_streamer_symbol('FOO'))

    @skip('TODO: this test is failing against certification environment. fix it.')
    def test_futures(self):
        translations = self.__factory.create(['/ESU3', '/NQU3', '/FOO'])
        self.assertIsNotNone(translations.get_streamer_symbol('/ESU3'))
        self.assertIsNotNone(translations.get_streamer_symbol('/NQU3'))
        self.assertIsNone(translations.get_streamer_symbol('/FOO'))

    def test_equity_options(self):
        translations = self.__factory.create(
            ['SPY   230630C00255000', 'SPY   230630P00255000', 'FOO   230630P00255000'])
        self.assertIsNotNone(translations.get_streamer_symbol('SPY   230630C00255000'))
        self.assertIsNotNone(translations.get_streamer_symbol('SPY   230630P00255000'))
        self.assertIsNone(translations.get_streamer_symbol('FOO   230630P00255000'))

    @skip('TODO: this test is failing against certification environment. fix it.')
    def test_future_options(self):
        translations = self.__factory.create(['./ESU3 EW2N3 230714C4310', './FOO9 EW4U9 190927P2975'])

        # TODO: this might eventually fail once the contract expires
        self.assertIsNotNone(translations.get_streamer_symbol('./ESU3 EW2N3 230714C4310'))

        self.assertIsNone(translations.get_streamer_symbol('./FOO9 EW4U9 190927P2975'))

    def test_cryptocurrencies(self):
        translations = self.__factory.create(['BTC/USD', 'ETH/USD', 'FOO/BAR'])
        self.assertIsNotNone(translations.get_streamer_symbol('BTC/USD'))
        self.assertIsNotNone(translations.get_streamer_symbol('ETH/USD'))
        self.assertIsNone(translations.get_streamer_symbol('FOO/BAR'))

    @skip('TODO: this test is failing against certification environment. fix it.')
    def test_multiple_instrument_types(self):
        translations = self.__factory.create(
            ['SPY', '/ESU3', 'SPY   230630C00255000', './ESU3 EW2N3 230714C4310', 'BTC/USD'])
        self.assertIsNotNone(translations.get_streamer_symbol('SPY'))
        self.assertIsNotNone(translations.get_streamer_symbol('/ESU3'))
        self.assertIsNotNone(translations.get_streamer_symbol('SPY   230630C00255000'))
        self.assertIsNotNone(translations.get_streamer_symbol('./ESU3 EW2N3 230714C4310'))
        self.assertIsNotNone(translations.get_streamer_symbol('BTC/USD'))
