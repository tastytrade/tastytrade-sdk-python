from injector import Injector

from tastytrade_sdk.accounts.accounts import Accounts
from tastytrade_sdk.config import Config
from tastytrade_sdk.api import Api, RequestsSession
from tastytrade_sdk.market_data.market_data import MarketData
from tastytrade_sdk.orders import Orders


class Tastytrade:
    """
    The SDK's top-level class
    """

    def __init__(self, api_base_url: str = 'api.tastytrade.com',
                 account_streaming_base_url: str = 'streamer.tastyworks.com'):
        """
        :param api_base_url: Optionally override the base URL used by the API
        :param account_streaming_base_url: Optionally override the base URL used for account streaming
        """

        def configure(binder):
            binder.bind(Config, to=Config(
                api_base_url=api_base_url,
                account_streaming_base_url=account_streaming_base_url
            ))

        self.__container = Injector(configure)

    def login(self, login: str, password: str) -> 'Tastytrade':
        """
        Initialize a logged-in session
        """
        self.__container.get(RequestsSession).login(login, password)
        return self

    def logout(self) -> None:
        """
        End the session
        """
        self.api.delete('/sessions')

    @property
    def accounts(self) -> Accounts:
        """@private"""
        return self.__container.get(Accounts)

    @property
    def orders(self) -> Orders:
        """@private"""
        return self.__container.get(Orders)

    @property
    def market_data(self) -> MarketData:
        """
        Access the MarketData submodule
        """
        return self.__container.get(MarketData)

    @property
    def api(self) -> Api:
        """
        Access the Api submodule
        """
        return self.__container.get(Api)
