from typing import Any, List, Callable, Optional

from tastytrade_sdk.websocket import Websocket


class AccountStreamer:
    def __init__(self, base_url: str, account_numbers: List[str], token: str):
        self.__account_numbers = account_numbers
        self.__token = token
        self.__websocket = Websocket(f'wss://{base_url}')

    def start(self, on_message: Callable[[dict], None], timeout_seconds: Optional[int] = None) -> 'AccountStreamer':
        self.__websocket.open(
            connect_action=lambda: self.__send('connect', self.__account_numbers),
            on_message=self.__wrap_on_message(on_message),
            keepalive_action=lambda: self.__send('heartbeat'),
            timeout_seconds=timeout_seconds
        )
        return self

    def stop(self) -> None:
        if self.__websocket:
            self.__websocket.close()

    def join(self) -> None:
        if self.__websocket:
            self.__websocket.join()

    @staticmethod
    def __wrap_on_message(on_message: Callable[[dict], None]) -> Callable:
        def __on_message(message: dict) -> None:
            if message.get('action') in ['connect', 'heartbeat']:
                return
            on_message(message)

        return __on_message

    def __send(self, action: str, value: Any = None) -> None:
        self.__websocket.send({
            'action': action,
            'value': value,
            'auth-token': self.__token
        })
