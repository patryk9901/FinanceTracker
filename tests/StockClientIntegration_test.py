import pytest
import os

from flask.cli import load_dotenv

from adapters.stockClient.DefaultStockClient import DefaultStockClient
from domain.Stock import Stock
from adapters.nbpclient.Money import Money
import requests

@pytest.mark.integration
def test_get_latest_price_integration():
    load_dotenv()
    api_key = os.getenv("STOCK_CLIENT_API_KEY")
    assert api_key, "Brak klucza API w .env"

    # Podgląd odpowiedzi surowej z API
    symbol = "AAPL"
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    print("RAW API RESPONSE:", response.text)  # <-- tutaj zobaczysz całą odpowiedź JSON

    client = DefaultStockClient()
    stock = Stock(ticker="AAPL", exchange="US", name="Apple Inc.", currency="USD")
    result = client.get_latest_price(stock)

    assert isinstance(result, Money)
    assert result.currency == "PLN"
    assert result.amount > 0

    print(f"Cena AAPL w PLN: {result}")
