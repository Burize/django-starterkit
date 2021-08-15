from typing import Type

import uritemplate
from django.urls import get_resolver
from rest_framework.request import Request

from template.api.argument_resolvers import ArgumentResolver
from template.api.core.routing import Route


class PathParametersArgumentResolver(ArgumentResolver):
    _url_resolver = get_resolver()

    @classmethod
    def is_supported(cls, route: Route, argument_name: str, argument_type: Type) -> bool:
        path_variables = uritemplate.variables(route.path)
        return argument_name in path_variables

    @classmethod
    def resolve_argument(cls, request: Request, route: Route, argument_name: str, argument_type: Type):
        if argument_name not in uritemplate.variables(route.path):
            raise Exception(f"Can't resolve {argument_name}")

        resolver_match = cls._url_resolver.resolve(request.path_info)

        callback, callback_args, callback_kwargs = resolver_match

        return argument_type(callback_kwargs[argument_name])




