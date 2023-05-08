from datetime import datetime
from typing import List, Optional

from injector import inject

from tastytrade_sdk.api import Api
from tastytrade_sdk.market_metrics.models import MarketMetric


class MarketMetrics:
    @inject
    def __init__(self, api: Api):
        self.__api = api

    def get_market_metrics(self, symbols: List[str] = tuple()) -> List[MarketMetric]:
        response = self.__api.get('/market-metrics', [('symbols', ','.join(s for s in symbols))])
        if not response:
            return []
        return [
            MarketMetric(
                symbol=x['symbol'],
                implied_volatility_percentile=self.__optional_float(x, 'implied-volatility-percentile'),
                implied_volatility_rank=self.__optional_float(x, 'implied-volatility-index-rank'),
                updated_at=datetime.strptime(x['updated-at'], '%Y-%m-%dT%H:%M:%S.%f%z') if 'updated-at' in x else None
            )
            for x in response['data']['items']
        ]

    @staticmethod
    def __optional_float(x: dict, key: str) -> Optional[float]:
        value = x.get(key)
        return None if value is None else float(value)
