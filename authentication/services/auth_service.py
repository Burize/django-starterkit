from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from django.contrib.auth import logout
from rest_framework.request import Request

from authentication.models import Account
from authentication.repositories import AccountRepository
from template.exceptions import NotFoundException


class AuthenticationException(BaseException):
    pass


class AuthService:
    def __init__(self):
        self._account_repository = AccountRepository()

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