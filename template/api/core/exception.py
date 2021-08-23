import functools
from typing import Callable
from typing import Type

from rest_framework.response import Response


def raises(exception_type: Type[Exception], http_code: int):
    def decorator(func: Callable):

        @functools.wraps(func)
        def wrapped_func(*args, **kwarg):
            try:
                return func(*args,  **kwarg)
            except exception_type as exc:
                return Response(exc.message, status=http_code)

        return wrapped_func
    return decorator
