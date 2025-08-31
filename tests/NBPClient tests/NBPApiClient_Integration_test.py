import pytest
from adapters.nbpclient.NBPApiClient import NBPApiClient
from decimal import Decimal

@pytest.mark.integration
def test_get_exchange_rate_integration():
    rate = NBPApiClient.get_exchange_rate("USD")
    assert isinstance(rate, Decimal)
    assert rate > 0