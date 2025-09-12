import pytest
from unittest.mock import patch, Mock
from decimal import Decimal
from adapters.nbpclient.NBPApiClient import NBPApiClient

@patch('adapters.nbpclient.NBPApiClient.requests.get')
def test_get_exchange_rate_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "table": "A",
        "currency": "dolar amerykański",
        "code": "USD",
        "rates": [{"no": "123/A/NBP/2025", "effectiveDate": "2025-08-11", "mid": 4.5}]
    }
    mock_get.return_value = mock_response

    rate = NBPApiClient.get_exchange_rate("USD")
    assert rate == Decimal('4.5')

@patch('adapters.nbpclient.NBPApiClient.requests.get')
def test_get_exchange_rate_not_found(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Brak kursu dla waluty"):
        NBPApiClient.get_exchange_rate("XXX")