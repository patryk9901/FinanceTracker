from domain.Portfolio import Portfolio
from domain.Stock import Stock
from domain.StockPosition import StockPosition
from adapters.nbpclient.Money import Money

def test_add_stock_position():
    #given
    portfolio = Portfolio.create()
    stock = Stock("1", "2", "stock", "PLN")
    stock_position = StockPosition(Money(21, "PLN"), 1, stock)

    #when
    portfolio.add_stock_position(stock_position)

    #then
    assert len(portfolio.stock_positions) == 1
    assert stock in portfolio.stock_positions

    saved_position = portfolio.stock_positions[stock]
    assert saved_position.quantity == 1
    assert saved_position.stock == stock
    assert saved_position.unit_price == Money(21, "PLN")


def test_add_stock_position_increase_quantity():
    #given
    portfolio = Portfolio.create()
    stock = Stock("2", "3", "stock1", "PLN")
    stock_position = StockPosition(Money(21, "PLN"), 1, stock)


    #when
    for _ in range(3):
        stock_position = StockPosition(Money(21, "PLN"), 1, stock)
        portfolio.add_stock_position(stock_position)

    #then
    assert len(portfolio.stock_positions) == 1
    assert stock in portfolio.stock_positions

    saved_position = portfolio.stock_positions[stock]
    assert saved_position.quantity == 3
    assert saved_position.stock == stock
    assert saved_position.unit_price == Money(21, "PLN")

def test_delete_stock_position():
    #given
    portfolio = Portfolio.create()
    stock = Stock("2", "3", "stock1", "PLN")
    stock_position = StockPosition(Money(21, "PLN"), 1, stock)
    portfolio.add_stock_position(stock_position)

    #when
    portfolio.delete_stock_position(stock_position)

    #then
    assert len(portfolio.stock_positions) == 0
    assert stock not in portfolio.stock_positions

def test_delete_stock_position_when_quantity_after_is_0():
    #given
    portfolio = Portfolio.create()
    stock = Stock("2", "3", "stock1", "PLN")
    stock_position = StockPosition(Money(21, "PLN"), 1, stock)
    portfolio.add_stock_position(stock_position)

    #when
    portfolio.delete_stock_position(stock_position,1)

    #then
    assert len(portfolio.stock_positions) == 0
    assert stock not in portfolio.stock_positions

def test_delete_stock_position_quantity():
    #given
    portfolio = Portfolio.create()
    stock = Stock("2", "3", "stock1", "PLN")
    stock_position = StockPosition(Money(21, "PLN"), 5, stock)
    portfolio.add_stock_position(stock_position)

    #when
    portfolio.delete_stock_position(stock_position,3)

    #then
    assert len(portfolio.stock_positions) == 1

    saved_position = portfolio.stock_positions[stock]
    assert saved_position.quantity == 2

def test_get_current_portfolio_value():
    #given
    portfolio = Portfolio.create()
    stock1 = Stock("2", "3", "stock1", "PLN")
    stock_position1 = StockPosition(Money(20, "PLN"), 5, stock1)

    stock2 = Stock("5", "1", "stock2", "PLN")
    stock_position2 = StockPosition(Money(10, "PLN"), 3, stock2)

    portfolio.add_stock_position(stock_position1)
    portfolio.add_stock_position(stock_position2)

    #when
    total_value = portfolio.get_current_portfolio_value()

    #then
    assert total_value == Money(130,"PLN")

