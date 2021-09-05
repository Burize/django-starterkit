from .base import *

TEST = True

ALLOWED_HOSTS = ['domain.test']
CSRF_COOKIE_SECURE = False

REST_FRAMEWORK['TEST_REQUEST_DEFAULT_FORMAT'] = 'json'


