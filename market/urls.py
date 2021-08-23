from market.controllers import OrderController
from market.controllers import ProductController
from template.api import create_urls

urlpatterns = [
    *create_urls(OrderController),
    *create_urls(ProductController),
]
