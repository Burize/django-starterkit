from typing import Type

from rest_framework.request import Request

from template.api.argument_resolvers import ArgumentResolver
from template.api.core.routing import Route
from template.api.decoders import json_decode


class RequestBodyArgumentResolver(ArgumentResolver):
    argument_name = 'request_body'

    @classmethod
    def is_supported(cls,  route: Route, argument_name: str, argument_type: Type) -> bool:
        if argument_name == cls.argument_name:
            return True
        return False

    @classmethod
    def resolve_argument(cls, request: Request, route: Route, argument_name: str, argument_type: Type):
        return json_decode(request.data, argument_type)
