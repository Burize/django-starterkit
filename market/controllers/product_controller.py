from dataclasses import dataclass
from uuid import UUID

from injector import inject

from market.queries import ProductQueries
from template import api


@dataclass
class ProductDTO:
    id: UUID
    name: int


@api.controller('products/')
class ProductController:
    @inject
    def __init__(
        self,
        product_queries: ProductQueries,
    ):
        self._product_queries = product_queries

    @api.permissions('market.view_product')
    @api.router_get('{?limit=10}')
    def list(self, limit: int):
        products = self._product_queries.get_list(limit=limit)

        return [ProductDTO(id=product.id, name=product.name) for product in products]
