from typing import List

from injector import inject

from tastytrade_sdk.accounts.models import PositionsParams
from tastytrade_sdk.accounts.account_streamer import AccountStreamer
from tastytrade_sdk.api import Api
from tastytrade_sdk.config import Config


class Accounts:
    @inject
    def __init__(self, api: Api, config: Config):
        self.__api = api
        self.__config = config

    def get_balances(self, account_number: str) -> dict:
        """
        https://developer.tastytrade.com/open-api-spec/balances-and-positions/#/accounts/getAccountsAccountNumberBalances
        """
        return self.__api.get(f'/accounts/{account_number}/balances')['data']

    def get_positions(self, account_number: str, params: PositionsParams) -> List[dict]:
        """
        https://developer.tastytrade.com/open-api-spec/balances-and-positions/#/positions/getAccountsAccountNumberPositions
        """
        return self.__api.get(f'/accounts/{account_number}/positions', params=params.to_params())['data']['items']

    def get_streamer(self, account_numbers: List[str]) -> AccountStreamer:
        return AccountStreamer(base_url=self.__config.account_streaming_base_url, account_numbers=account_numbers,
                               token=self.__api.token)
