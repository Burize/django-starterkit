import dataclasses
from  dataclasses import dataclass
from http import HTTPStatus

from authentication.services.auth_service import AuthenticationException
from template import api

from django.contrib.auth import login
from injector import inject
from rest_framework.request import Request
from rest_framework.response import Response

from authentication.dtos import AccountDTO
from authentication.services import AuthService


@dataclass
class LoginDTO:
    username: str
    password: str


@api.controller('')
@api.without_authentication
class AuthController:
    @inject
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    @api.router_post('login/', exceptions=[(AuthenticationException, HTTPStatus.UNAUTHORIZED)])
    def login(self, request: Request, request_body: LoginDTO):
        account = self._auth_service.authenticate(username=request_body.username, password=request_body.password)

        login(request, account.user)

        return AccountDTO(id=account.id, email=account.email)
