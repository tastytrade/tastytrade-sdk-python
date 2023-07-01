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
    username='jane.doe@email.com',
    password='password'
)

tasty.api.post('/sessions/validate')

tasty.logout()
```
