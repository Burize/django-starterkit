from uuid import UUID

from market.models import Order


class OrderQueries:
    def get_for_account(self, account_id: UUID):
        return Order.objects.filter(account_id=account_id).all()
