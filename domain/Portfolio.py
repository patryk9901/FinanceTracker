import uuid
from typing import Dict
from domain.Stock import Stock
from domain.StockPosition import StockPosition
from adapters.nbpclient.Money import Money


class Portfolio:
    def __init__(self, portfolio_id: uuid.UUID, stock_positions: Dict[Stock, StockPosition]):
        self.portfolio_id = portfolio_id
        self.stock_positions = stock_positions

    @classmethod
    def create(cls):
        return cls(portfolio_id=uuid.uuid4(), stock_positions={})

    def get_current_portfolio_value(self):
        total_value = Money(0,"PLN")
        for stock_position in self.stock_positions.values():
            total_value += stock_position.get_total_value()
        return total_value

    def add_stock_position(self, stock_position: StockPosition):
        if stock_position.stock in self.stock_positions:
            existing_position = self.stock_positions[stock_position.stock]
            existing_position.quantity += stock_position.quantity
        else:
            self.stock_positions[stock_position.stock] = stock_position

    def delete_stock_position(self,stock_position: StockPosition,quantity=None):
        if stock_position.stock not in self.stock_positions:
            raise KeyError(f"Stock {stock_position.stock.name} does not exists")
        existing_stock = self.stock_positions[stock_position.stock]
        if quantity is None:
            self.stock_positions.pop(stock_position.stock)
        else:
            if quantity > existing_stock.quantity:
                raise ValueError("Given quantity is bigger than actual amount of stock")
            existing_stock.quantity -= quantity
            if existing_stock.quantity == 0:
                self.stock_positions.pop(stock_position.stock)


    def get_stock_position(self, stock_position: StockPosition):
        if stock_position.stock not in self.stock_positions:
            raise KeyError(f"Stock {stock_position.stock.name} does not exists")
        return self.stock_positions.get(stock_position.stock)





