from collections import defaultdict
from typing import List
from typing import Type

from injector import Injector

from django.conf.urls import re_path
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from template.api.routing import ControllerClass
from template.api.routing import Route


def create_urls(_controller_class: Type) -> List:
    controller_class: ControllerClass = _controller_class
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


def _create_django_view(controller_class, routes: List[Route]):
    class View(APIView):
        authentication_classes = (SessionAuthentication,)
        permission_classes = (IsAuthenticated,)

    for route in routes:
        dispatch = _create_dispatch_function(controller_class, route)
        dispatch.route = route
        dispatch_method_name = route.http_method.lower()
        setattr(View, dispatch_method_name, dispatch)
    return View().as_view()


def _create_dispatch_function(controller_class, route: Route):

    def dispatch(view, request: Request):
        controller = Injector().get(controller_class)
        return _call_controller_method(controller, route.func, request)

    return dispatch


def _call_controller_method(controller, controller_method, request):
    return controller_method(controller, request)
