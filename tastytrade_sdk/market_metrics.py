from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from injector import inject

from tastytrade_sdk.api import Api


@dataclass
class MarketMetric:
    symbol: str
    implied_volatility_percentile: Optional[float]
    implied_volatility_rank: Optional[float]
    updated_at: datetime


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
                implied_volatility_percentile=float(x.get('implied-volatility-percentile')),
                implied_volatility_rank=float(x.get('implied-volatility-index-rank')),
                updated_at=datetime.strptime(x['updated-at'], '%Y-%m-%dT%H:%M:%S.%f%z')
            )
            for x in response['data']['items']
        ]
