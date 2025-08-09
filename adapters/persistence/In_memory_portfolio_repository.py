from domain.Portfolio_Repository import PortfolioRepository


class InMemoryPortfolioRepository(PortfolioRepository):
    def __init__(self):
        self.portfolios = dict()

    def get_portfolio(self, portfolio_id):
        return self.portfolios.get(portfolio_id)

    def save_portfolio(self, portfolio):
        self.portfolios[portfolio.portfolio_id] = portfolio