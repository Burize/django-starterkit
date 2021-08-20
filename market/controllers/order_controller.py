from dataclasses import dataclass
from uuid import UUID

from rest_framework import viewsets
from rest_framework.request import Request

from authentication.repositories import AccountRepository
from market.queries import OrderQueries
from template import api
from template.exceptions import ForbiddenException


@dataclass
class OrderDTO:
    id: UUID
    number: int


@api.controller('orders/')
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

    @api.router_get('{?limit=10}')
    def list(self, request: Request, limit: int):
        user_id = request.user.id
        account = self._account_repository.get_by_user_id(user_id)
        orders = self._order_queries.get_for_account(account.id, limit=limit)

        return [OrderDTO(id=order.id, number=order.number) for order in orders]

    @api.router_get('{order_id}')
    def list(self, request: Request, order_id: str):
        user_id = request.user.id
        account = self._account_repository.get_by_user_id(user_id)

        if not self._order_queries.is_belongs_to_user(order_id=order_id, account_id=account.id):
            raise ForbiddenException("This order doesn't belong to you")

        order_dto = self._order_queries.get_detailed(order_id=order_id)
        return order_dto

