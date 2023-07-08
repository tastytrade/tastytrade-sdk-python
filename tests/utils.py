from os import environ

from dotenv import load_dotenv

from tastytrade_sdk import Tastytrade

load_dotenv()


def get_tasty() -> Tastytrade:
    return Tastytrade(api_base_url=environ.get('API_BASE_URL')) \
        .login(environ.get('TASTYTRADE_LOGIN'), environ.get('TASTYTRADE_PASSWORD'))
