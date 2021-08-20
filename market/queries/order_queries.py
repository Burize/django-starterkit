from dataclasses import dataclass
from typing import Iterable
from typing import List
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from market.models import Order
from template.exceptions import NotFoundException


@dataclass
class OrderProductView:
    name: str
    amount: int


@dataclass
class OrderDetailedView:
    id: UUID
    number: int
    products:  List[OrderProductView]


class OrderQueries:
    def get_for_account(self, account_id: UUID, limit: int = 50) -> Iterable[Order]:
        return Order.objects.filter(account_id=account_id).all()[:limit]

    def is_belongs_to_user(self, order_id: UUID, account_id) -> bool:
        return Order.objects.filter(id=order_id, account_id=account_id).exists()

    def get_detailed(self, order_id: UUID) -> OrderDetailedView:
        try:
            order = Order.objects.prefetch_related('products').get(pk=order_id)

        except ObjectDoesNotExist:
            raise NotFoundException(f'Could not find order with id: {order_id}')

        order_products = order.products.select_related('product').all()

        products = [
            OrderProductView(name=order_products.product.name, amount=order_products.amount)
            for order_products in order_products]

        return OrderDetailedView(
            id=order.id,
            number=order.number,
            products=products
        )
