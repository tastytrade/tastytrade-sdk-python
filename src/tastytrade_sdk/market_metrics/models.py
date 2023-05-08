from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class MarketMetric:
    symbol: str
    implied_volatility_percentile: Optional[float]
    implied_volatility_rank: Optional[float]
    updated_at: Optional[datetime]
