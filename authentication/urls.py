from django.urls import path

from authentication.controllers import AuthController
from authentication.controllers import SignUpController

urlpatterns = [
    path('login/', AuthController.as_view({'post': 'login'})),
    path('signup/', SignUpController.as_view({'post': 'signUp'})),
]