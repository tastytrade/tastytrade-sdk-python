import logging
from typing import Optional, Tuple, List, Any, Union, Dict

from injector import singleton, inject
from requests import Session, JSONDecodeError

from tastytrade_sdk.config import Config
from tastytrade_sdk.exceptions import TastytradeSdkException

QueryParams = Union[Dict[str, Any], List[Tuple[str, Any]]]


@singleton
class RequestsSession:
    __session = Session()
    __user_agent = 'tastytrade-sdk-python'

    @inject
    def __init__(self, config: Config):
        self.__base_url = f'https://{config.api_base_url}'

    def login(self, login: str, password: str) -> None:
        self.__session.headers['Authorization'] = self.request(
            'POST',
            '/sessions',
            data={'login': login, 'password': password}
        )['data']['session-token']

    def request(self, method: str, path: str, params: Optional[QueryParams] = tuple(),
                data: Optional[dict] = None) -> Optional[dict]:
        url = self.__url(path, params)
        logging.debug('%s %s', path, params)
        response = self.__session.request(method, url, json=data, headers={'User-Agent': self.__user_agent})
        is_ok = 200 <= response.status_code <= 399
        if is_ok:
            try:
                return response.json()
            except JSONDecodeError:
                return None
        if response.status_code == 400:
            raise BadRequest()
        if response.status_code == 401:
            raise Unauthorized()
        if response.status_code >= 500:
            raise ServerError()
        raise Unknown()

    def __url(self, path: str, params: Optional[QueryParams] = None) -> str:
        url = f'{self.__base_url}{path}'
        if params:
            if isinstance(params, dict):
                params = list(params.items())
            url += '?' + '&'.join(f'{p[0]}={p[1]}' for p in params)
        return url


@singleton
class Api:
    """
    In case an open API feature isn't supported by this SDK yet, use this submodule to make direct requests to the API.

    The `params` argument can either be a `Dict[str, Any]` or a `List[Tuple[str, Any]]`

    API endpoints that accept multiple symbols in the query string use the `symbol[]=SPY&symbol[]=AAPL&...` convention,
    in which case, `params` should be passed as a `List[Tuple[str, Any]]`, since duplicate keys are not allowed in
    dicts. e.g:
    ```python
    equities = tasty.api.get(
        '/instruments/equities',
        params=[('symbol[]', 'SPY'), ('symbol[]', 'AAPL')]
    )
    ```
    <br/>
    """

    @inject
    def __init__(self, requests_session: RequestsSession):
        """@private"""
        self.__session = requests_session

    def get(self, path: str, params: Optional[QueryParams] = None) -> Optional[dict]:
        """Make a GET request"""
        return self.__session.request('GET', path, params=params)

    def post(self, path: str, params: Optional[QueryParams] = None, data: Optional[dict] = None) -> Optional[dict]:
        """Make a POST request"""
        return self.__session.request('POST', path, params=params, data=data)

    def put(self, path: str, params: Optional[QueryParams] = None, data: Optional[dict] = None) -> Optional[dict]:
        """Make a PUT request"""
        return self.__session.request('PUT', path, params=params, data=data)

    def patch(self, path: str, params: Optional[QueryParams] = None, data: Optional[dict] = None) -> Optional[dict]:
        """Make a PATCH request"""
        return self.__session.request('PATCH', path, params=params, data=data)

    def delete(self, path: str, params: Optional[QueryParams] = None) -> Optional[dict]:
        """Make a DELETE request"""
        return self.__session.request('DELETE', path, params=params)


class Unauthorized(TastytradeSdkException):
    def __init__(self):
        super().__init__('Unauthorized')


class BadRequest(TastytradeSdkException):
    def __init__(self):
        super().__init__('Bad Request')


class ServerError(TastytradeSdkException):
    def __init__(self):
        super().__init__('Server Error')


class Unknown(TastytradeSdkException):
    def __init__(self):
        super().__init__('Unknown Error')
