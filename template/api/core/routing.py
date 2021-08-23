import re
from typing import Callable
from typing import List
from typing import Literal
from typing import Optional
from typing import Protocol

from uritemplate import URITemplate
from uritemplate.variable import URIVariable

HTTPMethod = Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

_remove_query_params_regexp = re.compile(r'{\?[^}]*}')


class Route:
    def __init__(
        self,
        url: str,
        http_method: str,
        controller_method: Callable,
    ):
        self._url = url
        self.http_method = http_method
        self.controller_method = controller_method

    @property
    def url(self):
        return self._url

    @property
    def path(self):
        return _remove_query_params_regexp.sub('', self.url)

    @property
    def query_parameters(self) -> Optional[URIVariable]:
        uri_variables = [
            variable
            for variable in URITemplate(self.url).variables
            if variable.operator == '?'
        ]

        if uri_variables:
            return uri_variables[0]
        return None


class RouterDescriptor:
    def __init__(
        self,
        controller_method: Callable,
        url: str,
        http_method: HTTPMethod,
    ):
        self._controller_method = controller_method
        self._url = url
        self._http_method = http_method

    def __set_name__(self, cls, name):
        if not hasattr(cls, '_routes'):
            cls._routes = []
        cls._routes.append(Route(self._url, self._http_method, self._controller_method))

    def __call__(self, *args, **kwargs):
        self._controller_method(*args, **kwargs)


class APIControllerInterface(Protocol):
    _base_path: str
    _routes: List[Route]


def controller(base_path: str):
    def wrapped_class(cls):
        cls._base_path = base_path
        return cls

    return wrapped_class


def router_get(url: str):
    return _route(url, 'GET')


def router_post(url: str):
    return _route(url, 'POST')


def router_put(url: str):
    return _route(url, 'PUT')


def router_patch(url: str):
    return _route(url, 'PATCH')


def router_delete(url: str):
    return _route(url, 'DELETE')


def _route(url: str, http_method: HTTPMethod):
    def wrapped_method(func):
        return RouterDescriptor(func, url, http_method)

    return wrapped_method
