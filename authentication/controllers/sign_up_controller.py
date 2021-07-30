from django.db import transaction
from injector import inject
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from authentication.seriaizers import SignUpPayloadSerializer
from authentication.services import RegistrationService


class SignUpController(viewsets.ViewSet):
    @inject
    def __init__(self, registration_service: RegistrationService = RegistrationService()):
        self._registration_service = registration_service

    @transaction.atomic()
    def signUp(self, request: Request):
        serializer = SignUpPayloadSerializer(data=request.data)
        serializer.is_valid()

        credentials = serializer.validated_data
        self._registration_service.create_new_user(
            username=credentials['username'],
            email=credentials['email'],
            password=credentials['password'],
        )

        return Response(status=status.HTTP_200_OK)


