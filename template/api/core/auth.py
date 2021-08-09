from typing import Type


def without_authentication(cls: Type):
    cls._without_authentication = True
    return cls


def is_need_authentication(cls: Type):
    if not hasattr(cls, '_without_authentication'):
        return True

    return not cls._without_authentication
