from http import HTTPStatus

import pytest
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

from authentication.models import Account

endpoint = '/sign_up/'


@pytest.mark.db
def test_sign_up(api_client):
    dto = {'username': 'new_user', 'password': '1234', 'email': 'test@email.com'}

    # Act
    response = api_client.post(endpoint, data=dto)

    # Assert
    assert response.status_code == HTTPStatus.OK
    created_account = Account.objects.filter(user__username=dto['username']).first()
    assert created_account.email == dto['email']
    assert check_password(dto['password'], created_account.password)


@pytest.mark.db
def test_sign_up_bad_request_if_username_already_taken(api_client):
    already_taken_username = 'already_taken_username'
    user = User.objects.create(username=already_taken_username, password='1234')
    Account.objects.create(user=user, email='test_1@email.com')

    dto = {'username': already_taken_username, 'password': '1234', 'email': 'test_2@email.com'}

    # Act
    response = api_client.post(endpoint, data=dto)

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == 'This username already taken'


@pytest.mark.db
def test_sign_up_bad_request_if_email_already_taken(api_client):
    already_taken_email = 'taken_email@test.com'
    user = User.objects.create(username='userename', password='1234')
    Account.objects.create(user=user, email=already_taken_email)

    dto = {'username': 'new_user', 'password': '1234', 'email': already_taken_email}

    # Act
    response = api_client.post(endpoint, data=dto)

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == 'This email already taken'
