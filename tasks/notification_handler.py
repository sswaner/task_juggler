import requests

from dotenv import load_dotenv
import os

load_dotenv()

NTFY_URL = os.getenv("NTFY_URL")
NTFY_TOPIC = os.getenv("NTFY_TOPIC")

def send_ntfy(message):
    ntfy_url = f"{NTFY_URL}/{NTFY_TOPIC}"
    requests.post(ntfy_url,
                  data=message.encode(encoding='utf-8'))

if __name__ == "__main__":
    send_ntfy("Test message")
    print("Notification sent successfully")
