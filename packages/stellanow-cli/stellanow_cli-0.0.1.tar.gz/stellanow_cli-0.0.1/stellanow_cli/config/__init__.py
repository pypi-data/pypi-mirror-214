from enum import Enum

from .config import Config


class Env(Enum):
    INT = 'int'
    DEV = 'dev'

    @staticmethod
    def is_valid(value):
        return value in Env.__members__
