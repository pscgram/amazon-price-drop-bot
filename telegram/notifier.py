import os
import requests


class TelegramNotifier:

    def __init__(self):
        self.token = os.environ["BOT_TOKEN"]
        self.channel_id = os.environ["CHANNEL_ID"]

    def send_message(self, text):

        url = (
            f"https://api.telegram.org/"
            f"bot{self.token}/sendMessage"
        )

        data = {
            "chat_id": self.channel_id,
            "text": text
        }

        response = requests.post(
            url,
            json=data,
            timeout=20
        )

        response.raise_for_status()

        result = response.json()

        if not result.get("ok"):
            raise RuntimeError(result)

        return result
