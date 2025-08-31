import requests
from decimal import Decimal
import time

class NBPApiClient:
    _cache = {}
    _cache_ttl = 3600

    @classmethod
    def get_exchange_rate(cls, currency_code: str) -> Decimal:
        currency_code = currency_code.upper()
        now = time.time()

        if (currency_code in cls._cache and
                now - cls._cache[currency_code]['time'] < cls._cache_ttl):
            return cls._cache[currency_code]['rate']

        url = f'https://api.nbp.pl/api/exchangerates/rates/A/{currency_code}/?format=json'
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Brak kursu dla waluty {currency_code}")
        data = response.json()
        rate = Decimal(str(data['rates'][0]['mid']))

        cls._cache[currency_code] = {'rate': rate, 'time': now}
        return rate