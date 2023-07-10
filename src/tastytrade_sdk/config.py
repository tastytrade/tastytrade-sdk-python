from dataclasses import dataclass


@dataclass
class Config:
    """
    Global configuration for the SDK
    """
    api_base_url: str
    account_streaming_base_url: str
