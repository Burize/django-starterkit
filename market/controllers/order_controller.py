from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from authentication.repositories import AccountRepository
from market.queries import OrderQueries
from rest_framework import status


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

    def list(self, request: Request):
        user_id = request.user.id
        account = self._account_repository.get_by_user_id(user_id)

        orders = self._order_queries.get_for_account(account.id)

        return Response(status=status.HTTP_200_OK)
