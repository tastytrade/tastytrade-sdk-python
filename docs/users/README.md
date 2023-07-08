[![PyPI](https://img.shields.io/pypi/v/tastytrade-sdk)](https://pypi.org/project/tastytrade-sdk/)
[![GitHub Discussions](https://img.shields.io/github/discussions/tastytrade/tastytrade-sdk-python)](https://github.com/tastytrade/tastytrade-sdk-python/discussions)
[![GitHub issues](https://img.shields.io/github/issues/tastytrade/tastytrade-sdk-python)](https://github.com/tastytrade/tastytrade-sdk-python/issues)

# Getting Started

Before using this SDK, ensure that you:
* have a [Tastytrade account](https://start.tastytrade.com/)
* have opted into the [Tastytrade Open API program](https://developer.tastytrade.com/)

## Install

```shell
pip install tastytrade-sdk
```

## Use It

```python
from tastytrade_sdk import Tastytrade

tasty = Tastytrade()

tasty.login(
    login='trader@email.com',
    password='password'
)

tasty.api.post('/sessions/validate')

tasty.logout()
```

---

# Examples

## Streaming Market Data
```python
from tastytrade_sdk import Tastytrade
from tastytrade_sdk.market_data.models import Quote, Candle, Greeks

tasty = Tastytrade().login(login='trader@email.com', password='password')


# Define some event handlers
def on_quote(quote: Quote):
    print(quote)


def on_candle(candle: Candle):
    print(candle)


def on_greeks(greeks: Greeks):
    print(greeks)


# Subscribing to symbols across different instrument types
symbols = [
    'BTC/USD',
    'SPY',
    '/ESU3',
    'SPY   230630C00255000',
    './ESU3 EW2N3 230714C4310'
]

subscription = tasty.market_data.subscribe(
    symbols=symbols,
    on_quote=on_quote,
    on_candle=on_candle,
    on_greeks=on_greeks
)

# start streaming
subscription.open()
```