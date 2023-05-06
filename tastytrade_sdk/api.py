import json
from types import MappingProxyType
from typing import Optional, Any, Dict

import requests


class Api:
    __base_url = 'https://api.tastyworks.com'
    __token: Optional[str] = None

    def login(self, login: str, password: str) -> None:
        self.__token = requests.post(f'{self.__base_url}/sessions', data={
            'login': login,
            'password': password
        }).json()['data']['session-token']

    def get(self, path: str, params: Optional[Dict[str, Any]] = MappingProxyType({})) -> Optional[dict]:
        response = requests.get(
            f'{self.__base_url}{path}',
            params=params,
            headers={'Authorization': self.__token, 'content-type': 'application/json'}
        )
        if response.status_code == 404:
            return None
        return response.json()

    def put(self, path: str, payload: dict) -> dict:
        return requests.put(
            f'{self.__base_url}{path}',
            data=json.dumps(payload),
            headers={'Authorization': self.__token, 'content-type': 'application/json'}
        ).json()
