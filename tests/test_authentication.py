from os import environ
from unittest import TestCase

from tastytrade_sdk.api import Unauthorized
from tastytrade_sdk.tastytrade import Tastytrade


class Authentication(TestCase):
    def test_login_authentication(self):
        tasty = Tastytrade(api_base_url=environ.get('API_BASE_URL')) \
            .login(environ.get('TASTYTRADE_LOGIN'), environ.get('TASTYTRADE_PASSWORD'))
        tasty.api.post('/sessions/validate')
        tasty.logout()
        with self.assertRaises(Unauthorized):
            tasty.api.post('/sessions/validate')

    def test_oauth_authentication(self):
        tasty = Tastytrade.from_env()
        tasty.api.post('/sessions/validate')
