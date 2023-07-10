from dataclasses import dataclass
from typing import Optional, List, Tuple, Any


@dataclass
class PositionsParams:
    """@private"""
    underlying_symbols: Optional[List[str]] = None
    symbol: Optional[str] = None
    instrument_type: Optional[str] = None
    include_closed_positions: Optional[bool] = None
    underlying_product_code: Optional[str] = None
    partition_keys: Optional[List[str]] = None
    net_positions: Optional[bool] = None
    include_marks: Optional[bool] = None

    def to_params(self) -> List[Tuple[str, Any]]:
        params = []
        if self.underlying_symbols:
            params.extend([('underlying-symbols[]', x) for x in self.underlying_symbols])
        if self.symbol:
            params.append(('symbol', self.symbol))
        if self.instrument_type:
            params.append(('instrument-type', self.instrument_type))
        if self.include_closed_positions is not None:
            params.append(('include-closed-positions', self.include_closed_positions))
        if self.underlying_product_code:
            params.append(('underlying-product-code', self.underlying_product_code))
        if self.partition_keys:
            params.extend([('partition-keys[]', x) for x in self.partition_keys])
        if self.net_positions is not None:
            params.append(('net-positions', self.net_positions))
        if self.include_marks:
            params.append(('include-marks', self.include_marks))
        return params
