import pytest

from decimal import Decimal

from adapters.nbpclient.NBPApiClient import NBPApiClient


def test_get_exchange_rate_integration():
    rate = NBPApiClient.get_exchange_rate("USD")
    assert isinstance(rate, Decimal)
    assert rate > 0