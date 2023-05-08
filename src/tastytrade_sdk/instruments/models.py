from dataclasses import dataclass
from typing import List

from strenum import StrEnum


class Lendability(StrEnum):
    EASY_TO_BORROW = 'Easy To Borrow'
    HARD_TO_BORROW = 'Hard To Borrow'


@dataclass
class Equity:
    symbol: str


@dataclass
class CompactOptionChain:
    expiration_type: str
    symbols: List[str]
