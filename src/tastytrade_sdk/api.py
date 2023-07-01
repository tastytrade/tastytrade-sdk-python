import logging
from typing import Optional, Tuple, List, Any, Union, Dict

import importlib.metadata
from injector import singleton
from requests import Session, Response

from tastytrade_sdk.exceptions import TastytradeSdkException

QueryParams = Union[Dict[str, Any], List[Tuple[str, Any]]]


@singleton
class Api:
    __base_url = 'https://api.tastyworks.com'
    __session = Session()
    __user_agent = f'tastytrade-sdk-python v{importlib.metadata.version("tastytrade-sdk")}'

    def login(self, login: str, password: str) -> None:
        self.__session.headers['Authorization'] = self.post(
            '/sessions',
            data={'login': login, 'password': password}
        )['data']['session-token']

    def get(self, path: str, params: Optional[QueryParams] = None) -> Optional[dict]:
        return self.__request('GET', path, params=params).json()

    def post(self, path: str, params: Optional[QueryParams] = None, data: Optional[dict] = None) -> Optional[dict]:
        return self.__request('POST', path, params=params, data=data).json()

    def put(self, path: str, params: Optional[QueryParams] = None, data: Optional[dict] = None) -> Optional[dict]:
        return self.__request('PUT', path, params=params, data=data).json()

    def patch(self, path: str, params: Optional[QueryParams] = None, data: Optional[dict] = None) -> Optional[dict]:
        return self.__request('PATCH', path, params=params, data=data).json()

    def delete(self, path: str, params: Optional[QueryParams] = None) -> None:
        self.__request('DELETE', path, params=params)

    def __request(self, method: str, path: str, params: List[Tuple[str, Any]] = tuple(),
                  data: Optional[dict] = None) -> Response:
        url = self.__url(path, params)
        logging.debug('%s %s', path, params)
        response = self.__session.request(method, url, data=data, headers={'User-Agent': self.__user_agent})
        is_ok = 200 <= response.status_code <= 399
        if is_ok:
            return response
        if response.status_code == 400:
            raise BadRequest()
        if response.status_code == 401:
            raise Unauthorized()
        if response.status_code >= 500:
            raise ServerError()
        raise Unknown()

    def __url(self, path: str, params: Optional[Union[Dict[str, Any], List[Tuple[str, Any]]]] = None) -> str:
        url = f'{self.__base_url}{path}'
        if params:
            if isinstance(params, dict):
                params = list(params.items())
            url += '?' + '&'.join(f'{p[0]}={p[1]}' for p in params)
        return url


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
