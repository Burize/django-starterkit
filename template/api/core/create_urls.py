import dataclasses
from collections import Callable
from collections import defaultdict
from http import HTTPStatus
from typing import Any
from typing import List
from typing import Type

from injector import Injector

from django.conf.urls import re_path
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from template.api.argument_resolvers import ArgumentResolver
from template.api.argument_resolvers import HttpRequestArgumentResolver
from template.api.argument_resolvers import RequestBodyArgumentResolver
from template.api.core.auth import is_need_authentication
from template.api.core.routing import APIControllerInterface
from template.api.core.routing import Route


def create_urls(_controller_class: Type) -> List:
    controller_class: APIControllerInterface = _controller_class
    django_urls = []

    for url_path, routes in _group_routes_by_path(controller_class._routes):
        django_view = _create_django_view(controller_class, routes)
        url = controller_class._base_path + url_path
        django_urls.append(re_path(url, django_view))

    return django_urls


def _group_routes_by_path(routes: List[Route]):
    result = defaultdict(list)
    for route in routes:
        result[route.url].append(route)
    return result.items()


def _create_django_view(controller_class: APIControllerInterface, routes: List[Route]):
    class View(APIView):
        authentication_classes = (SessionAuthentication,)
        permission_classes = (IsAuthenticated, ) if is_need_authentication(controller_class) else ()

    for route in routes:
        dispatch = _create_dispatch_function(controller_class, route)
        dispatch.route = route
        dispatch_method_name = route.http_method.lower()
        setattr(View, dispatch_method_name, dispatch)
    return View().as_view()


def _create_dispatch_function(controller_class: APIControllerInterface, route: Route):

    def dispatch(view: APIView, request: Request):
        controller = Injector().get(controller_class)
        argument_resolvers = [HttpRequestArgumentResolver, RequestBodyArgumentResolver]
        return _call_controller_method(controller, route.controller_method, request, route, argument_resolvers)

    return dispatch


def _call_controller_method(
    controller: APIControllerInterface,
    controller_method: Callable,
    request: Request,
    route: Route,
    argument_resolvers: List[Type[ArgumentResolver]],
) -> Response:
    try:
        kwargs = {}

        for resolver in argument_resolvers:
            if resolver.is_supported(controller_method):
                kwargs[resolver.argument_name] = resolver.resolve_argument(request, controller_method)

        result = controller_method(controller, **kwargs)
        return _encode_result(result)
    except route.expected_exceptions as exception:
        return Response(exception.message, status=route.http_code_by_exception[type(exception)])


def _encode_result(result: Any) -> Response:
    if result is None:
        return Response(status=HTTPStatus.OK)

    if result is isinstance(result, Response):
        return result

    if result is HTTPStatus:
        return Response(status=result)

    if dataclasses.is_dataclass(result):
        return Response(dataclasses.asdict(result))

    return Response(result)
