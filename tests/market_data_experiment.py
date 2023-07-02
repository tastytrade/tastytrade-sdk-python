from tests.utils import get_tasty


def main():
    tasty = get_tasty()
    symbols = ['BTC/USD', 'SPY', 'ETH/USD', '/ESU3', 'SPY   230630C00255000', './ESU3 EW2N3 230714C4310', 'foo', 'bar']
    subscription = tasty.market_data.subscribe(symbols=symbols, on_quote=print, on_candle=print, on_greeks=print)
    subscription.open()


if __name__ == '__main__':
    main()
