import dataclasses

from template import api

from django.contrib.auth import login
from injector import inject
from rest_framework.request import Request
from rest_framework.response import Response

from authentication.dtos import AccountDTO
from authentication.seriaizers import LoginPayloadSerializer
from authentication.services import AuthService


@api.controller('')
class AuthController:
    @inject
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    @api.router_post('login/')
    def login(self, request: Request):
        serializer = LoginPayloadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        credentials = serializer.validated_data
        account = self._auth_service.authenticate(username=credentials['username'], password=credentials['password'])

        login(request, account.user)

        return Response(dataclasses.asdict(AccountDTO(id=account.id, email=account.email)))


