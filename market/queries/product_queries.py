from typing import Iterable

from market.models import Product


class ProductQueries:
    def get_list(self, limit: int = 50) -> Iterable[Product]:
        return Product.objects.all()[:limit]
