from dataclasses import dataclass

from .config import Config


@dataclass
class ConfigInt(Config):
    base_url: str = "https://api.int.stella.cloud"
