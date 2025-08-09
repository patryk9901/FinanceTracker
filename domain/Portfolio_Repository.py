from abc import ABC, abstractmethod

class PortfolioRepository(ABC):
    @abstractmethod
    def get_portfolio(self,portfolio_id):
        pass
    @abstractmethod
    def save_portfolio(self,portfolio):
        pass