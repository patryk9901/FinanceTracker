class Stock:
    def __init__(self, ticker, exchange, name, currency):
        self.ticker = ticker
        self.exchange = exchange
        self.name = name
        self.currency = currency

    def __eq__(self, other):
        if not isinstance(other, Stock):
            return False
        return (
                self.currency == other.currency
                and self.name == other.name
                and self.ticker == other.ticker
                and self.exchange == other.exchange
        )

    def __hash__(self):
        return hash((self.ticker, self.exchange, self.name, self.currency))