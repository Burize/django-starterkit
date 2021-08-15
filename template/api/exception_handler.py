import sys
from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.views import exception_handler as rf_exception_handler
from template.exceptions import NotFoundException

ERROR_500 = 'Sorry, something went wrong.'


def exception_handler(exc, context):
    if isinstance(exc, NotFoundException):
        return Response(exc.message, status=HTTPStatus.NOT_FOUND)

    default_handler_result = rf_exception_handler(exc, context)
    if default_handler_result:
        return default_handler_result

    response = Response(
        ERROR_500,
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
    response.exc_info = sys.exc_info()

    return response
