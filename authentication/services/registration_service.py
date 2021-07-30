from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from django.contrib.auth import logout
from rest_framework.request import Request

from authentication.models import Account
from authentication.repositories import AccountRepository
from template.exceptions import NotFoundException


class CreateNewUserException(BaseException):
    pass


class RegistrationService:
    def __init__(self):
        self._account_repository = AccountRepository()

    def create_new_user(self, username: str, email: str, password: str) -> Account:
        self._check_for_existence(username, email)

        account = self._account_repository.create(username, email, password)

        return account

    def _check_for_existence(self, username: str, email: str):
        is_username_already_taken = self._account_repository.exist_by_username(username)
        if is_username_already_taken:
            raise CreateNewUserException('This username already taken')

        is_username_already_taken = self._account_repository.exist_by_email(email)
        if is_username_already_taken:
            raise CreateNewUserException('This email already taken')