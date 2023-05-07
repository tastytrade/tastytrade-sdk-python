from os import environ
from unittest import TestCase

from dotenv import load_dotenv

from tastytrade_sdk import Tastytrade

load_dotenv()


class Experiment(TestCase):
    def test_experiment(self):
        tastytrade = Tastytrade()
        tastytrade.login(environ.get('TASTYTRADE_LOGIN'), environ.get('TASTYTRADE_PASSWORD'))
        for equity in tastytrade.instruments.get_active_equities():
            print(equity)
