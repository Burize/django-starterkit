from uuid import uuid4

from django.db import models

from template.models.common import TimestampedModel


class Product(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f'Product: {self.name}'
