from typing import get_type_hints
from typing import Any
from typing import List
from typing import Type

import uritemplate
from injector import Injector
from django.conf.urls import re_path

from collections import Callable
from collections import defaultdict
from http import HTTPStatus

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from template.api.argument_resolvers import ArgumentResolver
from template.api.argument_resolvers import HttpRequestArgumentResolver
from template.api.argument_resolvers import PathParametersArgumentResolver
from template.api.argument_resolvers import QueryParametersArgumentResolver
from template.api.argument_resolvers import RequestBodyArgumentResolver
from template.api.core.auth import is_need_authentication
from template.api.core.permissions import check_permission
from template.api.core.routing import APIControllerInterface
from template.api.core.routing import Route
from template.api.encoders import encode_dataclass

ARGUMENT_RESOLVERS = [
    HttpRequestArgumentResolver,
    RequestBodyArgumentResolver,
    PathParametersArgumentResolver,
    QueryParametersArgumentResolver,
]


def create_urls(_controller_class: Type) -> List:
    controller_class: Type[APIControllerInterface] = _controller_class
    django_urls = []

    for url_path, routes in _group_routes_by_path(controller_class._routes):
        django_view = _create_django_view(controller_class, routes)
        url = controller_class._base_path + rewrite_uritemplate_to_django_rest(url_path)
        django_urls.append(re_path(url, django_view))

    return django_urls


def _group_routes_by_path(routes: List[Route]):
    result = defaultdict(list)
    for route in routes:
        result[route.path].append(route)
    return result.items()


def _create_django_view(controller_class: Type[APIControllerInterface], routes: List[Route]):
    class View(APIView):
        authentication_classes = (SessionAuthentication,)
        permission_classes = (IsAuthenticated, ) if is_need_authentication(controller_class) else ()

    for route in routes:
        dispatch = _create_dispatch_function(controller_class, route)
        # dispatch.route = route
        dispatch_method_name = route.http_method.lower()
        setattr(View, dispatch_method_name, dispatch)
    return View().as_view()


def _create_dispatch_function(controller_class: Type[APIControllerInterface], route: Route):

    def dispatch(view: APIView, request: Request, **path_variables):
        controller: APIControllerInterface = Injector().get(controller_class)
        return _call_controller_method(controller, route.controller_method, request, route)

    return dispatch


def _call_controller_method(
    controller: APIControllerInterface,
    controller_method: Callable,
    request: Request,
    route: Route,
) -> Response:

    if route.has_permissions:
        for permission in route.permissions:
            check_permission(request.user, permission)

    kwargs = {}

    arguments = get_type_hints(controller_method)

    for (arg_name, arg_type) in arguments.items():
        resolver = _get_argument_resolver(route, arg_name, arg_type, ARGUMENT_RESOLVERS)
        kwargs[arg_name] = resolver.resolve_argument(request, route, arg_name, arg_type)

    result = controller_method(controller, **kwargs)
    return _encode_result(result)


def _get_argument_resolver(
    route: Route,
    argument_name: str,
    argument_type: Type,
    argument_resolvers: List[Type[ArgumentResolver]],
) -> Type[ArgumentResolver]:

    for resolver in argument_resolvers:
        if resolver.is_supported(route, argument_name, argument_type):
            return resolver

    raise Exception(f"Can't find resolver for argument {argument_name} of type {argument_type}")


def _encode_result(result: Any) -> Response:
    if result is None:
        return Response(status=HTTPStatus.OK)

    if isinstance(result, Response):
        return result

    if isinstance(result, HTTPStatus):
        return Response(status=result)

    encoded_result = encode_dataclass(result)

    return Response(encoded_result)


def rewrite_uritemplate_to_django_rest(url_path: str) -> str:
    default_regexp_for_parameter = r'[^/]+'
    for variable_name in uritemplate.variables(url_path):
        url_path = url_path.replace(f'{{{variable_name}}}', f'(?P<{variable_name}>{default_regexp_for_parameter})')

    return url_path
