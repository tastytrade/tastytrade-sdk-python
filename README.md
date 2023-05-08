![Read the Docs (version)](https://img.shields.io/readthedocs/tastytrade-sdk/latest?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dm/tastytrade-sdk?style=for-the-badge)
![PyPI - License](https://img.shields.io/pypi/l/tastytrade-sdk?style=for-the-badge)

# tastytrade-sdk-python

A python wrapper around the [tastytrade open API](https://developer.tastytrade.com/)

## Getting Started

### Install
```shell
pip install tastytrade-sdk
```

### Use It
```python
from tastytrade_sdk import Tastytrade

tastytrade = Tastytrade()

tastytrade.login(
    username='jane.doe@email..com',
    password='password'
)

tastytrade.instruments.get_active_equities()
```


## Read the Docs
https://tastytrade-sdk.readthedocs.io/