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
        self._permissions = []
        self._url = url
        self.http_method = http_method
        self.controller_method = controller_method

    def add_permission(self, permission: str):
        self._permissions.append(permission)

    @property
    def has_permissions(self):
        return bool(self._permissions)

    @property
    def permissions(self) -> List[str]:
        return self._permissions

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


class APIControllerInterface(Protocol):
    _base_path: str
    _routes: List[Route]


def controller(base_path: str):
    def wrapped_class(cls):
        cls._base_path = base_path
        cls._routes = [method._route for method in cls.__dict__.values() if hasattr(method, '_route')]
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
    def decorator(controller_method: Callable):
        controller_method._route = Route(url=url, http_method=http_method, controller_method=controller_method)
        return controller_method
    return decorator
