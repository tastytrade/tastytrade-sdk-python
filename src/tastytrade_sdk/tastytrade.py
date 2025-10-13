from os import environ
from typing import Optional
import warnings
from injector import Injector

from tastytrade_sdk.config import Config
from tastytrade_sdk.api import Api, RequestsSession
from tastytrade_sdk.market_data.market_data import MarketData


class Tastytrade:
    """
    The SDK's top-level class
    """

    def __init__(self,
                 api_base_url: str = 'api.tastytrade.com',
                 client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 refresh_token: Optional[str] = None):
        """
        :param api_base_url: Optionally override the base URL used by the API
        (when using the sandbox environment, for e.g.)
        """

        def __configure(binder):
            binder.bind(Config, to=Config(api_base_url=api_base_url,
                                          client_id=client_id,
                                          client_secret=client_secret,
                                          refresh_token=refresh_token))

        self.__container = Injector(__configure)

    def login(self, login: str, password: str) -> 'Tastytrade':
        """
        Initialize a logged-in session

        .. deprecated:: 1.3.0
            Use OAuth2 credentials instead.
        """
        self.__container.get(RequestsSession).login(login, password)
        return self

    def logout(self) -> None:
        """
        End the session

        .. deprecated:: 1.3.0
            Use OAuth2 credentials instead.
        """
        if self.__container.get(RequestsSession).is_oauth_session:
            warnings.warn('Logout does not need to be called with an OAuth2 session.', DeprecationWarning)
        else:
            self.api.delete('/sessions')

    @classmethod
    def from_env(cls) -> 'Tastytrade':
        """Creates a Tastytrade OAuth2 session using the environment variables:
    
        - `API_BASE_URL` (uses `api.tastyworks.com` unless specified)
        - `TT_CLIENT_ID`
        - `TT_CLIENT_SECRET`
        - `TT_REFRESH_TOKEN`
        """
        return Tastytrade(api_base_url=environ.get('API_BASE_URL', 'api.tastyworks.com'),
                          client_id=environ.get('TT_CLIENT_ID'),
                          client_secret=environ.get('TT_CLIENT_SECRET'),
                          refresh_token=environ.get('TT_REFRESH_TOKEN')
        )


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
