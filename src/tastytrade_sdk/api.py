import logging
from typing import Optional, Tuple, List, Any, Union, Dict

from injector import singleton, inject
from requests import Session, JSONDecodeError

from tastytrade_sdk.config import Config
from tastytrade_sdk.exceptions import TastytradeSdkException

QueryParams = Union[Dict[str, Any], List[Tuple[str, Any]]]

_LOGGER = logging.getLogger(__name__)


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
        _LOGGER.debug('%s %s', path, params)
        response = self.__session.request(method, url, json=data, headers={'User-Agent': self.__user_agent})
        is_ok = 200 <= response.status_code <= 399
        if is_ok:
            try:
                return response.json()
            except JSONDecodeError:
                return None
        try:
            error_data = response.json()['error']
        except (JSONDecodeError, KeyError):
            error_data = {'code': 'unknown', 'message': f'Could not parse response body: {response.text}'}

        if response.status_code == 400:
            error = BadRequest
        elif response.status_code == 401:
            error = Unauthorized
        elif response.status_code == 403:
            error = Forbidden
        elif response.status_code == 404:
            error = NotFound
        elif response.status_code == 422:
            error = Unprocessable
        elif response.status_code >= 500:
            error = ServerError
        else:
            error = HttpError
        raise error(response.reason, response.status_code, error_data)

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



class HttpError(TastytradeSdkException):
    def __init__(self, reason, http_code, data):
        error_code = data.get('code')
        error_message = data.get('message', 'No error message was provided.')
        if error_code and error_message:
            message = f"{error_code}: {error_message}"
        else:
            message = error_code or error_message
        super().__init__(f"{reason} ({http_code}) {message}")
        self.reason = reason
        self.http_code = http_code
        self.error_code = error_code
        self.error_message = error_message


class BadRequest(HttpError):
    pass


class Unauthorized(HttpError):
    pass


class Forbidden(HttpError):
    pass


class NotFound(HttpError):
    pass


class Unprocessable(HttpError):
    pass


class ServerError(HttpError):
    pass


# Provided for backwards compatibility
Unknown = HttpError