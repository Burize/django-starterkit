from django.urls import path

from rest_framework.routers import DefaultRouter
from market.controllers import OrderController

router = DefaultRouter()
router.register(r'orders', OrderController, basename='orders')

urlpatterns = router.urls
