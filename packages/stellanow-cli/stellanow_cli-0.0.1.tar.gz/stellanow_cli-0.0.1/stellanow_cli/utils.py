import re


def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)


def snake_to_lower_camel(s):
    components = s.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def remove_comments(code: str) -> str:
    return re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
