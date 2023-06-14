from abc import ABC


class TastytradeException(BaseException, ABC):
    def __init__(self, message: str):
        self.__message = message

    @property
    def message(self) -> str:
        return self.__message

    def __str__(self) -> str:
        return self.message


class Unauthorized(TastytradeException):
    def __init__(self):
        super().__init__('Unauthorized')


class BadRequest(TastytradeException):
    def __init__(self):
        super().__init__('Bad Request')


class ServerError(TastytradeException):
    def __init__(self):
        super().__init__('Server Error')


class Unknown(TastytradeException):
    def __init__(self):
        super().__init__('Unknown Error')
