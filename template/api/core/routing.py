from typing import Callable
from typing import List
from typing import Literal
from typing import Optional
from typing import Protocol
from typing import Tuple
from typing import Type

ExceptionMatchToCode = Tuple[Type[Exception], int]
HTTPMethod = Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE']


class Route:
    def __init__(
        self,
        url: str,
        http_method: str,
        controller_method: Callable,
        exceptions: Optional[List[ExceptionMatchToCode]] = (),
    ):
        self.url = url
        self.http_method = http_method
        self.controller_method = controller_method

        self._exceptions = exceptions
        self.http_code_by_exception = {exception[0]: exception[1] for exception in exceptions}
        self.expected_exceptions = tuple(self.http_code_by_exception)


class RouterDescriptor:
    def __init__(
        self,
        controller_method: Callable,
        url: str,
        http_method: HTTPMethod,
        exceptions: Optional[List[ExceptionMatchToCode]] = (),
    ):
        self._controller_method = controller_method
        self._url = url
        self._http_method = http_method
        self._exceptions = exceptions

    def __set_name__(self, cls, name):
        if not hasattr(cls, '_routes'):
            cls._routes = []
        cls._routes.append(Route(self._url, self._http_method, self._controller_method, self._exceptions))

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


def router_get(url: str, exceptions: Optional[List[ExceptionMatchToCode]] = ()):
    return _route(url, 'GET', exceptions=exceptions)


def router_post(url: str, exceptions: Optional[List[ExceptionMatchToCode]] = ()):
    return _route(url, 'POST', exceptions=exceptions)


def router_put(url: str, exceptions: Optional[List[ExceptionMatchToCode]] = ()):
    return _route(url, 'PUT', exceptions=exceptions)


def router_patch(url: str, exceptions: Optional[List[ExceptionMatchToCode]] = ()):
    return _route(url, 'PATCH', exceptions=exceptions)


def router_delete(url: str, exceptions: Optional[List[ExceptionMatchToCode]] = ()):
    return _route(url, 'DELETE', exceptions=exceptions)


def _route(url: str, http_method: HTTPMethod, exceptions: Optional[List[ExceptionMatchToCode]]):
    def wrapped_method(func):
        return RouterDescriptor(func, url, http_method, exceptions)

    return wrapped_method
