from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """
    Global configuration for the SDK
    """
    api_base_url: str
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    refresh_token: Optional[str] = None
