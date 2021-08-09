from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from injector import inject
from rest_framework.request import Request

from authentication.models import Account
from authentication.repositories import AccountRepository
from template.exceptions import CustomException
from template.exceptions import NotFoundException


class AuthenticationException(CustomException):
    @property
    def message(self):
        return self.args[0] if self.args else 'Username or password is incorrect'


class AuthService:
    @inject
    def __init__(self, account_repository: AccountRepository):
        self._account_repository = account_repository

    def login(self, request: Request, username: str, password: str):
        account = self.authenticate(username, password)
        login(request, account.user)

    def authenticate(self, username: str, password: str) -> Account:
        try:
            account = self._account_repository.get_by_username(username)
        except NotFoundException:
            raise AuthenticationException()

        password_is_valid = check_password(password, account.password)

        if not password_is_valid:
            raise AuthenticationException()

        return account
