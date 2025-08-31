from decimal import Decimal, InvalidOperation
from adapters.nbpclient.NBPApiClient import NBPApiClient

class Money:
    def __init__(self, amount, currency):
        if not isinstance(currency, str) or len(currency) != 3:
            raise ValueError("Waluta musi być 3-literowym kodem ISO, np. 'PLN'")

        self.original_currency = currency.upper()

        try:
            decimal_amount = Decimal(str(amount))
        except (InvalidOperation, ValueError):
            raise ValueError("Kwota musi być liczbą lub stringiem reprezentującym liczbę")

        if self.original_currency == 'PLN':
            self.amount = decimal_amount
            self.currency = 'PLN'
        else:
            rate = NBPApiClient.get_exchange_rate(self.original_currency)
            self.amount = decimal_amount * rate
            self.currency = 'PLN'

    def _check_currency(self, other):
        if not isinstance(other, Money):
            raise TypeError("Operacja wymaga obiektu Money")
        if self.currency != other.currency:
            raise ValueError("Waluty muszą być takie same")

    def __add__(self, other):
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        self._check_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return Money(self.amount * Decimal(str(other)), self.currency)
        raise TypeError("Można mnożyć tylko przez liczbę")

    def __truediv__(self, other):
        if isinstance(other, (int, float, Decimal)):
            other_dec = Decimal(str(other))
            if other_dec == 0:
                raise ZeroDivisionError("Nie można dzielić przez 0")
            return Money(self.amount / other_dec, self.currency)
        elif isinstance(other, Money):
            self._check_currency(other)
            if other.amount == 0:
                raise ZeroDivisionError("Nie można dzielić przez 0")
            return self.amount / other.amount  # zwraca Decimal (liczbę)
        else:
            raise TypeError("Dzielenie dozwolone tylko przez liczbę lub Money")

    def __eq__(self, other):
        if not isinstance(other, Money):
            return False
        return self.currency == other.currency and self.amount == other.amount

    def __lt__(self, other):
        self._check_currency(other)
        return self.amount < other.amount

    def __le__(self, other):
        self._check_currency(other)
        return self.amount <= other.amount

    def __gt__(self, other):
        self._check_currency(other)
        return self.amount > other.amount

    def __ge__(self, other):
        self._check_currency(other)
        return self.amount >= other.amount

    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"

    def __repr__(self):
        return f"Money(amount={self.amount}, currency='{self.currency}')"
