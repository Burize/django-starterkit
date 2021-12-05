from dataclasses import dataclass
from http import HTTPStatus
from uuid import UUID

from django.contrib.auth import logout

from authentication.services.auth_service import AuthenticationException
from template import api

from django.contrib.auth import login
from injector import inject
from rest_framework.request import Request

from authentication.services import AuthService


@dataclass
class LoginDTO:
    username: str
    password: str


@dataclass
class AccountDTO:
    id: UUID
    email: str


@api.controller('')
@api.without_authentication
class AuthController:
    @inject
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    @api.router_post('login/')
    @api.raises(AuthenticationException, HTTPStatus.UNAUTHORIZED)
    def login(self, request: Request, request_body: LoginDTO):
        account = self._auth_service.authenticate(username=request_body.username, password=request_body.password)

        login(request, account.user)

        return AccountDTO(id=account.id, email=account.email)

    @api.router_post('logout/')
    @api.raises(AuthenticationException, HTTPStatus.UNAUTHORIZED)
    def logout(self, request: Request):
        if not request.user.is_authenticated:
            raise AuthenticationException('Not logged in')

        logout(request)

