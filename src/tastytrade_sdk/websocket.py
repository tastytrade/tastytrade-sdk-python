import threading
import time
from typing import Optional, Callable

import ujson
from websockets.exceptions import ConnectionClosedOK
from websockets.sync.client import ClientConnection, connect


class LoopThread(threading.Thread):
    def __init__(self, activity: Callable, timeout_seconds: int = 0, run_immediately: bool = True):
        threading.Thread.__init__(self)
        self.__running = True
        self.__activity = activity
        self.__timeout_seconds = timeout_seconds
        if run_immediately:
            activity()
        super().start()

    def run(self):
        while self.__running:
            self.__pause()
            self.__activity()

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

    def __init__(self, url: str):
        self.__url = url
        self.__websocket: Optional[ClientConnection] = None
        self.__receive_thread: Optional[LoopThread] = None
        self.__keepalive_thread: Optional[LoopThread] = None
        self.__timeout_thread: Optional[LoopThread] = None

    def open(self, connect_action: Callable[[], None], on_message: Callable[[dict], None],
             keepalive_action: Callable[[], None], timeout_seconds: Optional[int] = None) -> None:
        self.__websocket = connect(self.__url)
        connect_action()
        self.__receive_thread = LoopThread(self.__wrap_on_message(on_message))
        self.__keepalive_thread = LoopThread(keepalive_action, timeout_seconds=15)
        if timeout_seconds:
            self.__timeout_thread = LoopThread(self.close, timeout_seconds=timeout_seconds)

    def close(self) -> None:
        if self.__keepalive_thread:
            self.__keepalive_thread.stop()
        if self.__receive_thread:
            self.__receive_thread.stop()
        if self.__timeout_thread:
            self.__timeout_thread.stop()
        if self.__websocket:
            self.__websocket.close()

    def join(self) -> None:
        if self.__keepalive_thread:
            self.__keepalive_thread.join()
        if self.__receive_thread:
            self.__receive_thread.join()
        if self.__timeout_thread:
            self.__timeout_thread.join()

    def send(self, data: dict) -> None:
        try:
            self.__websocket.send(ujson.dumps(data))
        except ConnectionClosedOK:
            pass

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
