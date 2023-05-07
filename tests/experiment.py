from os import environ
from unittest import TestCase

from dotenv import load_dotenv

from src.tastytrade_sdk import Tastytrade

load_dotenv()


class Experiment(TestCase):
    def test_experiment(self):
        tastytrade = Tastytrade()
        tastytrade.login(environ.get('TASTYTRADE_LOGIN'), environ.get('TASTYTRADE_PASSWORD'))
        for option_chain in tastytrade.instruments.get_compact_option_chains('AAPL'):
            print(option_chain)
