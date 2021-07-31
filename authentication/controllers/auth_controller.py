from dataclasses import dataclass
import dataclasses
from uuid import UUID

from django.contrib.auth import login
from injector import inject
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from authentication.seriaizers import LoginPayloadSerializer
from authentication.services import AuthService


@dataclass
class AccountDTO:
    id: UUID
    email: str


class AuthController(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @inject
    def __init__(self, auth_service: AuthService = AuthService()):
        self._auth_service = auth_service

    def login(self, request: Request):
        serializer = LoginPayloadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        credentials = serializer.validated_data
        account = self._auth_service.authenticate(username=credentials['username'], password=credentials['password'])

        login(request, account.user)

        return Response(dataclasses.asdict(AccountDTO(id=account.id, email=account.email)))


