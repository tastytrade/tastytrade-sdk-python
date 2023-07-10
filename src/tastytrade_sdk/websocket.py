import threading
import time
from typing import Optional, Callable

import ujson
from websockets.exceptions import ConnectionClosedOK
from websockets.sync.client import ClientConnection, connect


class LoopThread(threading.Thread):
    def __init__(self, activity: Callable, timeout_seconds: int = 0):
        threading.Thread.__init__(self)
        self.__running = True
        self.__activity = activity
        self.__timeout_seconds = timeout_seconds
        super().start()

    def run(self):
        while self.__running:
            self.__activity()
            self.__pause()

    def update_timeout_seconds(self, timeout_seconds: int) -> None:
        self.__timeout_seconds = timeout_seconds

    def __pause(self):
        if not self.__timeout_seconds:
            return
        start = time.time()
        while self.__running and time.time() - start <= self.__timeout_seconds:
            continue

    def stop(self):
        self.__running = False


class Websocket:
    __websocket: Optional[ClientConnection] = None
    __receive_thread: Optional[LoopThread]
    __keepalive_thread: Optional[LoopThread]

    def __init__(self, url: str):
        self.__url = url

    def open(self, connect_action: Callable[[], None], on_message: Callable[[dict], None],
             keepalive_action: Callable[[], None]) -> None:
        self.__websocket = connect(self.__url)
        connect_action()
        self.__receive_thread = LoopThread(self.__wrap_on_message(on_message))
        self.__keepalive_thread = LoopThread(keepalive_action, timeout_seconds=15)

    def close(self) -> None:
        if self.__keepalive_thread:
            self.__keepalive_thread.stop()
        if self.__receive_thread:
            self.__receive_thread.stop()
        if self.__websocket:
            self.__websocket.close()

    def send(self, data: dict) -> None:
        self.__websocket.send(ujson.dumps(data))

    def __wrap_on_message(self, on_message: Callable[[dict], None]) -> Callable[[], None]:
        def __receive() -> None:
            try:
                message = ujson.loads(self.__websocket.recv())
            except ConnectionClosedOK:
                return
            on_message(message)

        return __receive

    def update_keepalive_timeout_seconds(self, timeout_seconds: int) -> None:
        if self.__keepalive_thread:
            self.__keepalive_thread.update_timeout_seconds(timeout_seconds)
