
import os
import requests
from decimal import Decimal

from flask.cli import load_dotenv

from adapters.nbpclient.Money import Money
from adapters.nbpclient.NBPApiClient import NBPApiClient
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DefaultStockClient:
    def get_latest_price(self, stock):
        load_dotenv()
        api_key = os.getenv("STOCK_CLIENT_API_KEY")
        symbol = stock.ticker
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": api_key
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        logger.info(f"Odpowiedź API: {data}")

        if "Global Quote" not in data:
            raise ValueError(f"Brak danych 'Global Quote'. Pełna odpowiedź: {data}")

        price_string = data["Global Quote"]["05. price"]
        price = Decimal(price_string)
        price_pln = price * NBPApiClient.get_exchange_rate("EUR")

        return Money(price_pln, "PLN")
