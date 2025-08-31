from domain.Stock import Stock
from adapters.nbpclient.Money import Money

class StockPosition:
    def __init__(self, unit_price:Money, quantity, stock: Stock):
        self.unit_price = unit_price
        self.quantity = quantity
        self.stock = stock

    def get_total_value(self):
        return self.unit_price * self.quantity

    def __eq__(self, other):
        if not isinstance(other, StockPosition):
            return False
        return (
                self.unit_price == other.unit_price and
                self.quantity == other.quantity and
                self.stock == other.stock
        )

    def __hash__(self):
        return hash((self.unit_price, self.quantity, self.stock))
