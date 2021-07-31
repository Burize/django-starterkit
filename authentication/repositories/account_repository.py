from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from authentication.models import Account
from template.exceptions import NotFoundException


class AccountRepository:
    def create(self, username: str, email: str, password: str) -> Account:
        hashed_password = make_password(password)
        user = User.objects.create(username=username, password=hashed_password)
        account = Account.objects.create(email=email, user=user)
        return account

    def get_by_username(self, username: str) -> Account:
        account = Account.objects.filter(user__username=username).first()
        if not account:
            raise NotFoundException(f'Could not find account with username: {username}')

        return account

    def get_by_user_id(self, user_id: int) -> Account:
        account = Account.objects.filter(user_id=user_id).first()
        if not account:
            raise NotFoundException(f'Could not find account with user_id: {user_id}')

        return account

    def exist_by_username(self, username: str) -> bool:
        return Account.objects.filter(user__username=username).exists()

    def exist_by_email(self, email: str) -> bool:
        return Account.objects.filter(email=email).exists()
