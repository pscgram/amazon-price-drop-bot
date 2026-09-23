import json
import logging
from pathlib import Path

from providers.price_provider import PriceProvider, PriceProviderError
from telegram.notifier import TelegramNotifier


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

PRODUCTS_FILE = Path("products.json")
STATE_FILE = Path("state.json")


def load_json(file):
    if not file.exists():
        return {}
    
    with file.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(file, data):
    with file.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def main():

    products = load_json(PRODUCTS_FILE)
    state = load_json(STATE_FILE)

    provider = PriceProvider()
    telegram = TelegramNotifier()

    for product in products:

        if not product.get("enabled", True):
            continue

        product_id = product["id"]

        try:
            result = provider.get_price(product)

        except PriceProviderError as error:
            logging.error(
                "Price provider error for %s: %s",
                product_id,
                error
            )
            continue

        new_price = result.price

        old_price = state.get(product_id, {}).get("price")

        logging.info(
            "%s | old=%s | new=%s",
            product_id,
            old_price,
            new_price
        )

        if old_price is not None and new_price < old_price:

            drop = old_price - new_price

            drop_percent = (drop / old_price) * 100

            min_rupees = product.get("min_drop_rupees", 0)
            min_percent = product.get("min_drop_percent", 0)

            if drop >= min_rupees and drop_percent >= min_percent:

                message = (
                    "🔥 PRICE DROP ALERT!\n\n"
                    f"📦 {product['title']}\n\n"
                    f"💰 Previous: ₹{old_price:,.0f}\n"
                    f"🔥 Now: ₹{new_price:,.0f}\n"
                    f"📉 Drop: ₹{drop:,.0f} "
                    f"({drop_percent:.1f}%)\n\n"
                    f"🔗 {product['affiliate_url']}\n\n"
                    "As an Amazon Associate, we earn from "
                    "qualifying purchases."
                )

                telegram.send_message(message)

                logging.info(
                    "Telegram alert sent for %s",
                    product_id
                )

        state[product_id] = {
            "price": new_price,
            "checked_at": result.checked_at,
            "source": result.source
        }

    save_json(STATE_FILE, state)


if __name__ == "__main__":
    main()
