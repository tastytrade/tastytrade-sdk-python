from typing import Optional, Tuple, List, Any

from injector import singleton
from requests import Session, Response

from tastytrade_sdk.exceptions import Unauthorized, BadRequest, ServerError, Unknown


@singleton
class Api:
    __base_url = 'https://api.tastyworks.com'
    __session = Session()

    def login(self, login: str, password: str) -> None:
        self.__session.headers['Authorization'] = self.post(
            '/sessions',
            data={'login': login, 'password': password}
        )['data']['session-token']

    def get(self, path: str, params: List[Tuple[str, Any]] = tuple()) -> Optional[dict]:
        return self.__request('GET', path, params=params).json()

    def post(self, path: str, data: Optional[dict] = None) -> Optional[dict]:
        return self.__request('POST', path, data=data).json()

    def put(self, path: str, data: dict) -> Optional[dict]:
        return self.__request('PUT', path, data=data).json()

    def delete(self, path: str) -> None:
        self.__request('DELETE', path)

    def __request(self, method: str, path: str, params: List[Tuple[str, Any]] = tuple(),
                  data: Optional[dict] = None) -> Response:
        response = self.__session.request(method, self.__url(path, params), data=data)
        is_ok = 200 <= response.status_code <= 399
        if is_ok:
            return response
        if response.status_code == 400:
            raise BadRequest()
        if response.status_code == 401:
            raise Unauthorized()
        if response.status_code <= 500:
            raise ServerError()
        raise Unknown()

    def __url(self, path: str, params: List[Tuple[str, Any]] = tuple()) -> str:
        url = f'{self.__base_url}{path}'
        if params:
            url += '?' + '&'.join(f'{p[0]}={p[1]}' for p in params)
        return url
