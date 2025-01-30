import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "your_telegram_token_here")

API_TOKEN = os.getenv("API_TOKEN", "sandbox_api_token_here")

WHITELISTED_USER_IDS = set()
