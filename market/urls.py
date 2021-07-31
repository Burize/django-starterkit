from market.controllers import OrderController
from template.api import create_urls

urlpatterns = [
    *create_urls(OrderController),
]
