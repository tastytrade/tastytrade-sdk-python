[![PyPI](https://img.shields.io/pypi/v/tastytrade-sdk)](https://pypi.org/project/tastytrade-sdk/)
[![GitHub Discussions](https://img.shields.io/github/discussions/tastytrade/tastytrade-sdk-python)](https://github.com/tastytrade/tastytrade-sdk-python/discussions)
[![GitHub issues](https://img.shields.io/github/issues/tastytrade/tastytrade-sdk-python)](https://github.com/tastytrade/tastytrade-sdk-python/issues)

# Getting Started

Before using this SDK, ensure that you:
* have a [Tastytrade account](https://open.tastytrade.com/)
* have opted into the [Tastytrade Open API program](https://developer.tastytrade.com/)
* Have a set of OAuth2 client credentials and a refresh token for your personal OAuth2 app. See [Tastytrade OAuth2](https://developer.tastytrade.com/oauth/) for more details.

## Install

```shell
pip install tastytrade-sdk
```

## Use It

```python
from tastytrade_sdk import Tastytrade


tasty = Tastytrade(
    client_id = YOUR_CLIENT_ID,
    client_secret = YOUR_CLIENT_SECRET,
    refresh_token = YOUR_REFRESH_TOKEN,
)

tasty.api.post('/sessions/validate')
```

---

# Examples

## Streaming Market Data
```python
from tastytrade_sdk import Tastytrade

# Instead of creating a Tastyworks object manually, you can store the details in the following
# environment variables and call this to create the object automatically. Remember, never store
# your client secret or refresh token directly in code or check it into version control.
# To use the sandbox environment instead, use api.cert.tastyworks.com as the API_BASE_URL and
# be sure to use client credentials generated for that environment.
#  API_BASE_URL=api.tastyworks.com
#  TT_CLIENT_ID=
#  TT_CLIENT_SECRET=
#  TT_REFRESH_TOKEN=

tasty = Tastytrade.from_env()

# Subscribing to symbols across different instrument types
# Please note: The option symbols here are expired. You need to subscribe to an unexpired symbol to receive quote data
symbols = [
    'BTC/USD',
    'SPY',
    '/ESU3',
    'SPY   230630C00255000',
    './ESU3 EW2N3 230714C4310'
]

subscription = tasty.market_data.subscribe(
    symbols=symbols,
    on_quote=print,
    on_candle=print,
    on_greeks=print
)

# start streaming
subscription.open()
```