from dataclasses import dataclass

from .config import Config


@dataclass
class ConfigDev(Config):
    base_url: str = "https://api.dev-aws.stella.cloud"
