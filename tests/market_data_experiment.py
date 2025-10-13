import logging
import os
from tastytrade_sdk import Tastytrade


def main():
    logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO').upper())
    tasty = Tastytrade.from_env()
    symbols = ['YELP  240517C00042000', 'AAPL']
    subscription = tasty.market_data.subscribe(
        symbols=symbols, on_quote=print, on_candle=print, on_greeks=print,
        aggregation_period=1.5, event_fields={'Quote': ['askPrice', 'eventSymbol']})
    subscription.open()


if __name__ == '__main__':
    main()
