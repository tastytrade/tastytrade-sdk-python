# Getting Started

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

tasty = Tastytrade().login(login='trader@email.com', password='password')


# Define some event handlers
def on_quote(quote: Quote):
    print(quote)


def on_candle(candle: Candle):
    print(candle)


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
    on_candle=on_candle
)

# start streaming
subscription.open()
```