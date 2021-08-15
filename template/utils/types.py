from typing import Union
from typing import get_origin

NoneType = type(None)


def is_union(type_: object) -> bool:
    return get_origin(type_) == Union


def is_optional(type_: object) -> bool:
    return is_union(type_) and NoneType in getattr(type_, '__args__', [])