from os import environ
from unittest import TestCase

from dotenv import load_dotenv

from tastytrade_sdk import Tastytrade
from tastytrade_sdk.exceptions import Unauthorized, BadRequest

load_dotenv()


class Experiment(TestCase):
    def test_experiment(self):
        tastytrade = Tastytrade()
        auth = tastytrade.authentication
        auth.login(environ.get('TASTYTRADE_LOGIN'), environ.get('TASTYTRADE_PASSWORD'))
        auth.validate()

        with self.assertRaises(BadRequest):
            list(tastytrade.instruments.get_active_equities(lendability='Foobar'))

        auth.logout()

        with self.assertRaises(Unauthorized):
            auth.validate()
