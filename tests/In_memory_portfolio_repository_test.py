from adapters.persistence.In_memory_portfolio_repository import InMemoryPortfolioRepository
from domain.Portfolio import Portfolio




def test_save_portfolio():
    # given
    repo = InMemoryPortfolioRepository()
    portfolio = Portfolio.create("5000")


    # when
    repo.save_portfolio(portfolio)


    # then
    assert portfolio.portfolio_id in repo.portfolios


def test_get_portfolio():
    # given
    repo = InMemoryPortfolioRepository()
    portfolio = Portfolio.create("5000")
    repo.save_portfolio(portfolio)

    # when
    retrieved_portfolio = repo.get_portfolio(portfolio.portfolio_id)

    # then
    assert retrieved_portfolio.portfolio_id == portfolio.portfolio_id