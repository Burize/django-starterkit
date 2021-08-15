from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import Type

from rest_framework.request import Request

from template.api.core.routing import Route


class ArgumentResolver(ABC):
    @classmethod
    @abstractmethod
    def is_supported(cls, route: Route, argument_name: str, argument_type: Type) -> bool:
        pass

    @classmethod
    @abstractmethod
    def resolve_argument(cls, request: Request, route: Route, argument_name: str, argument_type: Type):
        pass
