from uuid import uuid4
from template.models.common import TimestampedModel
from django.db import models


class OrderProduct(TimestampedModel):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order_id', 'product_id'], name='unique_order_product')
        ]

    id = models.UUIDField(primary_key=True, default=uuid4)
    amount = models.PositiveIntegerField(null=False, default=0)
    order = models.ForeignKey('Order', related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return f'OrderProduct: {self.id}'
