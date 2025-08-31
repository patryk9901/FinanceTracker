from unittest import TestCase
from unittest.mock import patch
from decimal import Decimal
from adapters.nbpclient.Money import Money

class TestMoney(TestCase):

    def test_creation_pln(self):
        m = Money("100.50", "PLN")
        self.assertEqual(m.currency, "PLN")
        self.assertEqual(m.amount, Decimal("100.50"))
        self.assertEqual(m.original_currency, "PLN")

    @patch('adapters.nbpclient.Money.NBPApiClient.get_exchange_rate')
    def test_creation_usd(self, mock_get_rate):
        mock_get_rate.return_value = Decimal("4.5")
        m = Money(50, "USD")
        self.assertEqual(m.currency, "PLN")
        self.assertEqual(m.original_currency, "USD")
        self.assertEqual(m.amount, Decimal("225.0"))

    @patch('adapters.nbpclient.Money.NBPApiClient.get_exchange_rate')
    def test_addition(self, mock_get_rate):
        mock_get_rate.return_value = Decimal("4.0")
        m1 = Money(100, "PLN")
        m2 = Money(10, "USD")
        result = m1 + m2
        self.assertEqual(result.amount, Decimal("140"))
        self.assertEqual(result.currency, "PLN")

    def test_invalid_currency_code(self):
        with self.assertRaises(ValueError):
            Money(10, "EU")

    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            Money("abc", "PLN")

    def test_multiplication(self):
        m = Money("10", "PLN")
        result = m * 3
        self.assertEqual(result.amount, Decimal("30"))

    def test_division(self):
        m = Money("30", "PLN")
        result = m / 3
        self.assertEqual(result.amount, Decimal("10"))

    def test_division_by_zero(self):
        m = Money("10", "PLN")
        with self.assertRaises(ZeroDivisionError):
            m / 0

    def test_comparisons(self):
        m1 = Money("10", "PLN")
        m2 = Money("20", "PLN")
        self.assertTrue(m1 < m2)
        self.assertTrue(m2 > m1)
        self.assertTrue(m1 <= m1)
        self.assertTrue(m2 >= m1)

    def test_equality(self):
        m1 = Money("10", "PLN")
        m2 = Money("10", "PLN")
        m3 = Money("20", "PLN")
        self.assertEqual(m1, m2)
        self.assertNotEqual(m1, m3)