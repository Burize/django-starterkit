from http import HTTPStatus

import pytest
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from authentication.models import Account

login_endpoint = '/login/'
logout_endpoint = '/logout/'


@pytest.mark.db
def test_login(api_client):
    username = 'test_user'
    password = '1234'
    user = User.objects.create(username=username, password=make_password(password))
    account = Account.objects.create(user=user, email='test_1@email.com')

    dto = {'username': username, 'password': password}

    # Act
    response = api_client.post(login_endpoint, data=dto)

    # Assert
    assert response.status_code == HTTPStatus.OK
    result = response.data
    assert result['id'] == account.id
    assert result['email'] == account.email


@pytest.mark.db
def test_logout(api_client):
    user = User.objects.create(username='test_user', password='1234')

    api_client.force_login(user)

    # Act
    response = api_client.post(logout_endpoint)

    # Assert
    assert response.status_code == HTTPStatus.OK


@pytest.mark.db
def test_logout_error_if_not_logged_in(api_client):
    # Act
    response = api_client.post(logout_endpoint)

    # Assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == 'Not logged in'
