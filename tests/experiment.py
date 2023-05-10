from unittest import TestCase

from dotenv import load_dotenv

load_dotenv()


class Experiment(TestCase):
    def test_experiment(self):
        pass
        # tastytrade = Tastytrade()
        # tastytrade.login(environ.get('TASTYTRADE_LOGIN'), environ.get('TASTYTRADE_PASSWORD'))
        # for equity in tastytrade.instruments.get_active_equities(lendability=Lendability.EASY_TO_BORROW):
        #     print(equity)
