from typing import Callable
from typing import List
from typing import Protocol

class Route:
    def __init__(self, url: str, http_method: str, func: Callable):
        self.url = url
        self.http_method = http_method
        self.func = func


class RouterDescriptor:

    def __init__(self, func, url, http_method):
        self._func = func
        self._url = url
        self._http_method = http_method

    def __set_name__(self, cls, name):
        if not hasattr(cls, '_routes'):
            cls._routes = []
        cls._routes.append(Route(self._url, self._http_method, self._func))

    def __call__(self, *args, **kwargs):
        self._func(*args, **kwargs)


class ControllerClass(Protocol):
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


def _route(url: str, http_method: str):
    def wrapped_method(func):
        return RouterDescriptor(func, url, http_method)

    return wrapped_method
