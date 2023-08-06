"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

This software is the proprietary information of Stella Technologies (UK) Limited.
Use, reproduction, or redistribution of this software is strictly prohibited without
the express written permission of Stella Technologies (UK) Limited.
All rights reserved.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class StellaEntity:
    id: str
    name: str


@dataclass
class StellaField:
    id: str
    name: str
    valueType: str


@dataclass
class StellaEvent:
    id: str
    name: str
    isActive: bool
    createdAt: str
    updatedAt: str


@dataclass
class StellaEventDetailed(StellaEvent):
    description: str
    fields: List[StellaField]
    entities: List[StellaEntity]