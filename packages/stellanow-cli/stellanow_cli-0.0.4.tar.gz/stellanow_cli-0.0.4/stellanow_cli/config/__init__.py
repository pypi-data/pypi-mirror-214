"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

This software is the proprietary information of Stella Technologies (UK) Limited.
Use, reproduction, or redistribution of this software is strictly prohibited without
the express written permission of Stella Technologies (UK) Limited.
All rights reserved.
"""

from enum import Enum

from .config import Config


class Env(Enum):
    INT = 'int'
    DEV = 'dev'

    @staticmethod
    def is_valid(value):
        return value in Env.__members__
