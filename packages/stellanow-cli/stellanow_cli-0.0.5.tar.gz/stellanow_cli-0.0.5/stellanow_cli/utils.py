"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

This software is the proprietary information of Stella Technologies (UK) Limited.
Use, reproduction, or redistribution of this software is strictly prohibited without
the express written permission of Stella Technologies (UK) Limited.
All rights reserved.
"""

import re


def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)


def snake_to_lower_camel(s):
    components = s.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def remove_comments(code: str) -> str:
    return re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
