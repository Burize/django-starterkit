from .base import *

HEROKU_APP_HOST = os.getenv('HEROKU_APP_NAME', 'template') + '.herokuapp.com'

DEBUG = True

ALLOWED_HOSTS = [
    HEROKU_APP_HOST
]
