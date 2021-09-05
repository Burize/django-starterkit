from http import HTTPStatus

import pytest
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from authentication.models import Account

endpoint = '/login/'


@pytest.mark.db
def test_login(api_client):
    username = 'test_user'
    password = '1234'
    user = User.objects.create(username=username, password=make_password(password))
    account = Account.objects.create(user=user, email='test_1@email.com')

    dto = {'username': username, 'password': password}

    # Act
    response = api_client.post(endpoint, data=dto)

    # Assert
    assert response.status_code == HTTPStatus.OK
    result = response.data
    assert result['id'] == account.id
    assert result['email'] == account.email
