from abc import ABC
from abc import abstractmethod
from typing import Callable

from rest_framework.request import Request


class ArgumentResolver(ABC):
    argument_name: str

    @classmethod
    @abstractmethod
    def is_supported(cls, controller_method: Callable) -> bool:
        pass

    @classmethod
    @abstractmethod
    def resolve_argument(cls, request: Request, controller_method: Callable):
        pass
