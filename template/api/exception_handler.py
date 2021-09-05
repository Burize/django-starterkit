import sys
from http import HTTPStatus

from django.conf.urls import handler404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import exception_handler as rf_exception_handler

from template.api.decoders import BaseDecodeException
from template.exceptions import ForbiddenException
from template.exceptions import NotFoundException
from template.exceptions import PermissionException

ERROR_500 = 'Sorry, something went wrong.'


def exception_handler(exc, context):
    if isinstance(exc, NotFoundException):
        return Response(exc.message, status=HTTPStatus.NOT_FOUND)

    if isinstance(exc, ForbiddenException):
        return Response(exc.message or 'Access denied', status=HTTPStatus.FORBIDDEN)

    if isinstance(exc, PermissionException):
        return Response(exc.message or 'Access denied', status=HTTPStatus.FORBIDDEN)

    if isinstance(exc, BaseDecodeException):
        return Response(exc.message, status=HTTPStatus.BAD_REQUEST)

    default_handler_result = rf_exception_handler(exc, context)
    if default_handler_result:
        return default_handler_result

    response = Response(
        ERROR_500,
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
    response.exc_info = sys.exc_info()

    return response


def handle_not_found_path(request, exception=None):
    return JsonResponse("Requested url wasn't found", status=HTTPStatus.NOT_FOUND, safe=False)
