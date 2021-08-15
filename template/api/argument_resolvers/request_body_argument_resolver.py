from typing import Callable
from typing import get_type_hints

from rest_framework.request import Request

from template.api.argument_resolvers import ArgumentResolver
from template.api.decoders import json_decode


class RequestBodyArgumentResolver(ArgumentResolver):
    argument_name = 'request_body'

    @classmethod
    def is_supported(cls, controller_method: Callable) -> bool:
        type_hints = get_type_hints(controller_method)

        if cls.argument_name in type_hints.keys():
            return True
        return False

    @classmethod
    def resolve_argument(cls, request: Request, controller_method: Callable):
        argument_type = get_type_hints(controller_method)[cls.argument_name]
        return json_decode(request.data, argument_type)
