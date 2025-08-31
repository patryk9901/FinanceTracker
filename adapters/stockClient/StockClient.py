from abc import ABC, abstractmethod
from domain.Stock import Stock

class StockClient(ABC):
    @abstractmethod
    def get_latest_price(self,stock: Stock):
        pass


