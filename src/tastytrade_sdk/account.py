from typing import List, Optional

from tastytrade_sdk import Api


class Account:
    def __init__(self, account_number: str, api: Api):
        self.__account_number = account_number
        self.__api = api

    @property
    def balances(self) -> dict:
        """
        https://developer.tastytrade.com/open-api-spec/balances-and-positions/#/accounts/getAccountsAccountNumberBalances
        """
        return self.__api.get(f'/accounts/{self.__account_number}/balances')['data']

    def get_positions(self, underlying_symbols: Optional[List[str]] = None, symbol: Optional[str] = None,
                      instrument_type: Optional[str] = None, include_closed_positions: Optional[bool] = None,
                      underlying_product_code: Optional[str] = None, partition_keys: Optional[List[str]] = None,
                      net_positions: Optional[bool] = None, include_marks: Optional[bool] = None) -> List[dict]:
        """
        https://developer.tastytrade.com/open-api-spec/balances-and-positions/#/positions/getAccountsAccountNumberPositions
        """
        params = []
        if underlying_symbols:
            params.extend([('underlying-symbols[]', x) for x in underlying_symbols])
        if symbol:
            params.append(('symbol', symbol))
        if instrument_type:
            params.append(('instrument-type', instrument_type))
        if include_closed_positions is not None:
            params.append(('include-closed-positions', include_closed_positions))
        if underlying_product_code:
            params.append(('underlying-product-code', underlying_product_code))
        if partition_keys:
            params.extend([('partition-keys[]', x) for x in partition_keys])
        if net_positions is not None:
            params.append(('net-positions', net_positions))
        if include_marks:
            params.append(('include-marks', include_marks))

        return self.__api.get(f'/accounts/{self.__account_number}/positions', params=params)['data']['items']
