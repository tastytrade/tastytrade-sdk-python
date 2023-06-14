from dataclasses import dataclass
from typing import List


@dataclass
class Equity:
    symbol: str


@dataclass
class CompactOptionChain:
    expiration_type: str
    symbols: List[str]
