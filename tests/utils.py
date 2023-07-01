from os import environ

from dotenv import load_dotenv

from tastytrade_sdk import Tastytrade

load_dotenv()


def get_tasty() -> Tastytrade:
    return Tastytrade().login(environ.get('TASTYTRADE_LOGIN'), environ.get('TASTYTRADE_PASSWORD'))
