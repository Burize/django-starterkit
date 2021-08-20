from uuid import uuid4

from authentication.models import Account
from template.models.common import TimestampedModel
from django.db import models


class Order(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4)
    number = models.PositiveIntegerField(unique=True, null=False)

    account = models.ForeignKey(Account, related_name='orders', on_delete=models.CASCADE)

    def __str__(self):
        return f'Order: {self.number}'
