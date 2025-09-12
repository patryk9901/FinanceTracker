from unittest.mock import patch, Mock
from decimal import Decimal
from adapters.stockClient.DefaultStockClient import DefaultStockClient
from domain.Stock import Stock
from adapters.nbpclient.Money import Money

@patch('adapters.stockClient.DefaultStockClient.requests.get')
@patch('adapters.stockClient.DefaultStockClient.NBPApiClient.get_exchange_rate')
def test_get_latest_price_mock(mock_get_exchange_rate, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
    "Global Quote": {
        "05. price": "150.00"
    }
}
    mock_requests_get.return_value = mock_response

    mock_get_exchange_rate.return_value = Decimal('4.5')

    client = DefaultStockClient()
    client.api_key = "FAKE_KEY"

    stock = Stock(ticker="AAPL", exchange="US", name="Apple Inc.", currency="USD")

    result = client.get_latest_price(stock)

    assert isinstance(result, Money)
    assert result.currency == "PLN"
    assert result.amount == Decimal('675.00')
    args, kwargs = mock_requests_get.call_args
    assert kwargs['params']['symbol'] == "AAPL"