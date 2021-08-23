from typing import Callable

from django.contrib.auth.models import User

from template.exceptions import PermissionException


def permissions(permission: str):
    def decorator(method: Callable):

        if not hasattr(method, '_route'):
            raise Exception('permissions decorator can be used only for route method')
        method._route.add_permission(permission)

        return method

    return decorator


def check_permission(user: User, permission: str):
    if not user.has_perm(permission):
        raise PermissionException()
