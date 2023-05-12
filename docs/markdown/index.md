# Getting Started

## Install
```shell
pip install tastytrade-sdk
```

## Use It
```python
from tastytrade_sdk import Tastytrade

tastytrade = Tastytrade()

tastytrade.login(
    username='jane.doe@email.com',
    password='password'
)

tastytrade.instruments.get_active_equities()
```
