from http import HTTPStatus

import pytest
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from uritemplate import URITemplate

from market.models import Product

endpoint_uri_template = URITemplate('/market/products/{?limit}')


@pytest.mark.db
def test_get_product(api_client):
    product_1 = Product.objects.create(name='product_1')
    product_2 = Product.objects.create(name='product_2')
    product_3 = Product.objects.create(name='product_3')

    user = User.objects.create(username='test_user', password='1234')
    permission_to_view_product = Permission.objects.filter(codename='view_product').first()
    user.user_permissions.add(permission_to_view_product)

    api_client.force_login(user)

    expected_data = [
        {'id': str(product_1.id), 'name': product_1.name},
        {'id': str(product_2.id), 'name': product_2.name},
        {'id': str(product_3.id), 'name': product_3.name},
    ]

    # Act
    response = api_client.get(endpoint_uri_template.expand())

    # Assert
    assert response.status_code == HTTPStatus.OK
    products = response.json()
    assert len(products) == 3
    assert products == expected_data


@pytest.mark.db
def test_get_product_limit(api_client):
    Product.objects.create(name='product_1')
    Product.objects.create(name='product_2')
    Product.objects.create(name='product_3')
    Product.objects.create(name='product_4')
    Product.objects.create(name='product_5')

    user = User.objects.create(username='test_user', password='1234')
    permission_to_view_product = Permission.objects.filter(codename='view_product').first()
    user.user_permissions.add(permission_to_view_product)

    api_client.force_login(user)

    # Act
    response = api_client.get(endpoint_uri_template.expand(limit=2))

    # Assert
    assert response.status_code == HTTPStatus.OK
    products = response.json()
    assert len(products) == 2


@pytest.mark.db
def test_get_product_forbidden_without_permission(api_client):
    user = User.objects.create(username='test_user', password='1234')
    api_client.force_login(user)

    # Act
    response = api_client.get(endpoint_uri_template.expand())

    # Assert
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.data == 'Access denied'
