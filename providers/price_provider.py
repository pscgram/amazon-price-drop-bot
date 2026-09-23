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

        # FREE TEST PRICE
        test_price = 899

        return PriceResult(
            price=test_price,
            checked_at=datetime.now(timezone.utc).isoformat(),
            source="free-test"
        )
