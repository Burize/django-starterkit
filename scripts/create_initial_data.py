from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User

from authentication.models import Account
from market.models import Order
from market.models import OrderProduct
from market.models import Product


def _create_products():
    Product.objects.create(name='bag of grain 200g')
    Product.objects.create(name='coffee machine Miele CM6350 Black Obsidian')
    Product.objects.create(name='axe gardena 2800s')


def _create_users():
    users = [
        ('user_1', '1234', 'user_1@emai.com'),
        ('user_2', '1234', 'user_2@emai.com'),
        ('user_3', '1234', 'user_3@emai.com'),
    ]

    for username, password, email in users:
        hashed_password = make_password(password)
        user = User.objects.create(username=username, password=hashed_password)
        Account.objects.create(email=email, user=user)

    manager_group = Group(name='product_manager')
    manager_group.save()

    permission_names = ['view_product', 'change_product', 'add_product', 'delete_product']
    permissions = Permission.objects.filter(codename__in=permission_names).all()
    manager_group.permissions.set(permissions)

    user_1 = User.objects.filter(username='user_1').first()
    user_1.groups.add(manager_group)


def _create_orders():
    orders = [
        ('user_1', 1, 2),
        ('user_1', 2, 1),
        ('user_2', 3, 1),
    ]

    products = Product.objects.all()

    for username, serial_number, amount in orders:
        account = Account.objects.filter(user__username=username).first()

        order = Order.objects.create(number=serial_number, account=account)
        OrderProduct.objects.create(order=order, product=products[serial_number - 1], amount=amount)


def run():
    _create_products()
    _create_users()
    _create_orders()




