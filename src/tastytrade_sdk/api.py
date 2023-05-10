import json
from typing import Optional, Tuple, List, Any

import requests
from injector import singleton


@singleton
class Api:
    __base_url = 'https://api.tastyworks.com'
    __timeout_seconds = 15
    __token: Optional[str] = None

    def login(self, login: str, password: str) -> None:
        self.__token = requests.post(f'{self.__base_url}/sessions', data={
            'login': login,
            'password': password
        }, timeout=self.__timeout_seconds).json()['data']['session-token']

    def get(self, path: str, params: List[Tuple[str, Any]] = tuple()) -> Optional[dict]:
        response = requests.get(
            self.__url(path, params),
            headers=self.__headers(),
            timeout=self.__timeout_seconds
        )
        if response.status_code == 404:
            return None
        return response.json()

    def put(self, path: str, payload: dict) -> dict:
        return requests.put(
            f'{self.__base_url}{path}',
            data=json.dumps(payload),
            headers=self.__headers(),
            timeout=self.__timeout_seconds
        ).json()

    def __url(self, path: str, params: List[Tuple[str, Any]] = tuple()) -> str:
        url = f'{self.__base_url}{path}'
        if params:
            url += '?' + '&'.join(f'{p[0]}={p[1]}' for p in params)
        return url

    def __headers(self) -> dict:
        return {'Authorization': self.__token, 'content-type': 'application/json'}
