import pytest
from django.contrib.auth.models import User
from injector import Injector

from authentication.models import Account
from authentication.repositories import AccountRepository
from authentication.services import RegistrationService
from authentication.services.registration_service import CreateNewUserException


@pytest.mark.db
def test_create_create_new_user():
    registration_service = _get_registration_service()

    username = 'new user'
    email = 'new_user@email.com'
    password = '1234'

    # Act
    created_account = registration_service.create_new_user(username=username, email=email, password=password)

    # Assert
    assert created_account.user.username == username
    assert created_account.email == email


@pytest.mark.db
def test_create_create_new_user_raise_error_if_email_already_taken():
    taken_email = 'test@email.com'
    user = User.objects.create(username='username', password='password')
    Account.objects.create(email=taken_email, user=user)

    registration_service = _get_registration_service()

    # Act
    with pytest.raises(CreateNewUserException, match='This email already taken'):
        registration_service.create_new_user(username='new_username', email=taken_email, password='1234')


@pytest.mark.db
def test_create_create_new_user_raise_error_if_username_already_taken():
    taken_username = 'username'
    user = User.objects.create(username=taken_username, password='password')
    Account.objects.create(email='test_1@email.com', user=user)

    registration_service = _get_registration_service()

    # Act
    with pytest.raises(CreateNewUserException, match='This username already taken'):
        registration_service.create_new_user(username=taken_username, email='test_2@email.com', password='1234')


def _get_registration_service():
    service = RegistrationService(
        account_repository=Injector().get(AccountRepository)
    )

    return service
