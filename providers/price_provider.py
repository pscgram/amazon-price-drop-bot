from dataclasses import dataclass
from datetime import datetime, timezone


class PriceProviderError(Exception):
    pass


@dataclass
class PriceResult:
    price: float
    checked_at: str
    source: str


class PriceProvider:

    def get_price(self, product):
        """
        This is the price-provider interface.

        We will connect an authorized Amazon price-data source here.
        """

        raise PriceProviderError(
            "Price provider is not configured yet."
        )
