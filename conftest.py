import pytest
from rest_framework.test import APIClient


@pytest.fixture()
def api_client() -> APIClient:
    return APIClient(enforce_csrf_checks=False, SERVER_NAME='domain.test', HTTP_HOST='domain.test')


def pytest_collection_modifyitems(items):
    for item in items:
        if item.get_closest_marker('db'):
            item.add_marker(pytest.mark.django_db)


def pytest_runtest_setup(item):
    if item.get_closest_marker('skip'):
        return


def pytest_runtest_teardown(item, nextitem):
    if item.get_closest_marker('skip'):
        return

