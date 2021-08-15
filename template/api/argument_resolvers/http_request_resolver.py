from typing import Type

from rest_framework.request import Request

from template.api.argument_resolvers import ArgumentResolver
from template.api.core.routing import Route


class HttpRequestArgumentResolver(ArgumentResolver):
    @classmethod
    def is_supported(cls, route: Route, argument_name: str, argument_type: Type) -> bool:
        if argument_type == Request:
            return True
        return False

    @classmethod
    def resolve_argument(cls, request: Request, route: Route, argument_name: str, argument_type: Type):
        return request
