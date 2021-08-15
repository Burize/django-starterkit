from typing import Type

import uritemplate
from django.urls import get_resolver
from rest_framework.request import Request

from template.api.argument_resolvers import ArgumentResolver
from template.api.core.routing import Route
from template.api.decoders import json_decode
from template.utils.types import is_optional


class QueryParametersArgumentResolver(ArgumentResolver):
    _url_resolver = get_resolver()

    @classmethod
    def is_supported(cls, route: Route, argument_name: str, argument_type: Type) -> bool:
        if not route.query_parameters:
            return False

        return argument_name in route.query_parameters.variable_names

    @classmethod
    def resolve_argument(cls, request: Request, route: Route, argument_name: str, argument_type: Type):
        if not route.query_parameters or argument_name not in route.query_parameters.variable_names:
            raise Exception(f"Can't resolve {argument_name} from query parameters")

        request_query_parameters = request.query_params

        if argument_name in request_query_parameters:
            return json_decode(request_query_parameters[argument_name], argument_type)

        if argument_name in route.query_parameters.defaults:
            return json_decode(route.query_parameters.defaults[argument_name], argument_type)
        
        if is_optional(argument_type):
            return None

        raise Exception('Empty value for argument_name')
