from injector import inject

from tastytrade_sdk.api import Api


class Authentication:
    @inject
    def __init__(self, api: Api):
        self.__api = api

    def login(self, login: str, password: str) -> None:
        """
        Start a logged-in session.
        """
        self.__api.login(login, password)

    def validate(self) -> None:
        """
        Validate that the current login session is still valid.
        """
        self.__api.post('/sessions/validate')

    def logout(self) -> None:
        """
        Log out the current session.
        """
        self.__api.delete('/sessions')
