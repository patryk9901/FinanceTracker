import uuid
class Portfolio:
    def __init__(self, portfolio_id, value):
        self.portfolio_id = portfolio_id
        self.value = value
    @classmethod
    def create(value):
        return Portfolio(uuid.uuid4(), value)