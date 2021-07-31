from template.api import create_urls

from authentication.controllers import AuthController
from authentication.controllers import SignUpController

urlpatterns = [
    *create_urls(AuthController),
    *create_urls(SignUpController),
]
