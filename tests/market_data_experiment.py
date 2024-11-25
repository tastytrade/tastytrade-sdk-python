import logging
import os
from tests.utils import get_tasty


def main():
    logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO').upper())
    tasty = get_tasty()
    symbols = ['YELP  240517C00042000', 'AAPL']
    subscription = tasty.market_data.subscribe(
        symbols=symbols, on_quote=print, on_candle=print, on_greeks=print,
        aggregation_period=1.5, event_fields={'Quote': ['askPrice', 'eventSymbol']})
    subscription.open()


if __name__ == '__main__':
    main()
