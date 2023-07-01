from abc import ABC


class TastytradeSdkException(BaseException, ABC):
    def __init__(self, message: str):
        self.__message = message

    @property
    def message(self) -> str:
        return self.__message

    def __str__(self) -> str:
        return self.message


class InvalidArgument(TastytradeSdkException):
    def __init__(self, context: str):
        super().__init__(f'Invalid Argument: {context}')
