import inspect
from typing import Callable
from typing import get_type_hints

from rest_framework.request import Request

from template.api.argument_resolvers import ArgumentResolver


class HttpRequestArgumentResolver(ArgumentResolver):
    argument_name = 'request'

    @classmethod
    def is_supported(cls, controller_method: Callable) -> bool:
        type_hints = get_type_hints(controller_method)

        if cls.argument_name not in type_hints.keys():
            return False

        argument = type_hints[cls.argument_name]
        return inspect.isclass(argument) and issubclass(argument, Request)

    @classmethod
    def resolve_argument(cls, request: Request, controller_method: Callable):
        return request
