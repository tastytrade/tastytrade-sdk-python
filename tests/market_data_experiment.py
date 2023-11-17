import time

from tests.utils import get_tasty


def main():
    tasty = get_tasty()
    symbols = ['YELP  240517C00042000', 'AAPL']
    subscription = tasty.market_data.subscribe(symbols=symbols, on_quote=print, on_candle=print, on_greeks=print, on_trade=print)
    subscription.open()


if __name__ == '__main__':
    main()
