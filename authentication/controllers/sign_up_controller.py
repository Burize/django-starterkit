from dataclasses import dataclass
from http import HTTPStatus

from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from injector import inject

from authentication.services.registration_service import CreateNewUserException
from template import api
from authentication.services import RegistrationService


@dataclass
class SighUpDTO:
    username: str
    email: str
    password: str


@api.controller('')
@api.without_authentication
class SignUpController:
    @inject
    def __init__(self, registration_service: RegistrationService):
        self._registration_service = registration_service

    @api.router_post('sign_up')
    @api.raises(CreateNewUserException, HTTPStatus.BAD_REQUEST)
    @transaction.atomic()
    def signUp(self, request_body: SighUpDTO):
        self._registration_service.create_new_user(
            username=request_body.username,
            email=request_body.email,
            password=request_body.password,
        )
