import pytest
from adapters.controller.portfolio_controller import app
from adapters.persistence.In_memory_portfolio_repository import InMemoryPortfolioRepository
from domain.Portfolio import Portfolio

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_post_portfolio_controller(client):
    create_response = client.post('/portfolio', json={})
    response_data = create_response.get_json()

    assert create_response.status_code == 201
    assert "portfolioId" in response_data
    assert isinstance(response_data["stockPositions"], dict)
    assert response_data["success"] == "portfolio is added"


def test_get_portfolio_controller_fail(client):
    response = client.get('/portfolio')
    assert response.status_code == 400
    assert response.get_json() == {"error": "uuid parameter missing"}

def test_get_portfolio_controller(client):
    create_response = client.post('/portfolio', json={})
    assert create_response.status_code == 201
    portfolio_id = create_response.get_json()["portfolioId"]

    get_response = client.get(f'/portfolio?portfolioId={portfolio_id}')
    response_data = get_response.get_json()

    assert get_response.status_code == 200
    assert response_data["portfolioId"] == portfolio_id
    assert isinstance(response_data["stockPositions"], dict)

def test_save_portfolio():
    repo = InMemoryPortfolioRepository()
    portfolio = Portfolio.create()

    repo.save_portfolio(portfolio)

    assert portfolio.portfolio_id in repo.portfolios


def test_get_portfolio():
    repo = InMemoryPortfolioRepository()
    portfolio = Portfolio.create()
    repo.save_portfolio(portfolio)

    retrieved_portfolio = repo.get_portfolio(portfolio.portfolio_id)

    assert retrieved_portfolio.portfolio_id == portfolio.portfolio_id
