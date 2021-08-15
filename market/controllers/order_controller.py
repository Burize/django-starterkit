from typing import Optional

from rest_framework import viewsets
from rest_framework.request import Request

from authentication.repositories import AccountRepository
from market.queries import OrderQueries

from template import api


@api.controller('orders/')
@api.without_authentication
class OrderController(viewsets.ViewSet):
    def __init__(
        self,
        account_repository: AccountRepository = AccountRepository(),
        order_queries: OrderQueries = OrderQueries(),
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._account_repository = account_repository
        self._order_queries = order_queries

    @api.router_get('{order_id}/{?limit=10,order}')
    def list(self, request: Request, order_id: int, limit: str, order: Optional[int]):
        user_id = request.user.id
        account = self._account_repository.get_by_user_id(user_id)

        orders = self._order_queries.get_for_account(account.id)
