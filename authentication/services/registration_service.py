from injector import inject

from authentication.models import Account
from authentication.repositories import AccountRepository
from template.exceptions import CustomException


class CreateNewUserException(CustomException):
    pass


class RegistrationService:
    @inject
    def __init__(self, account_repository: AccountRepository):
        self._account_repository = account_repository

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
