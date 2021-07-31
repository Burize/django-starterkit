from uuid import uuid4

from authentication.models import Account
from market.models.product import Product
from template.models.common import TimestampedModel
from django.db import models


class Order(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4)
    number = models.IntegerField()
    client = models.ForeignKey(Account, related_name='orders', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
