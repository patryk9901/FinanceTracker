import pytest
from adapters.controller.portfolio_controller import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_post_portfolio_controller_fail(client):
    create_response = client.post('/portfolio', json={})
    assert create_response.status_code == 400
    assert create_response.get_json() == {"error": "value parameter missing"}

def test_post_portfolio_controller(client):
    create_response = client.post('/portfolio', json={"value": 1000})
    response_data = create_response.get_json()

    assert create_response.status_code == 201
    assert "portfolioId" in response_data
    assert response_data["portfolioValue"] == 1000
    assert response_data["success"] == "portfolio is added"


def test_get_portfolio_controller_fail(client):
    response = client.get('/portfolio')
    assert response.status_code == 400
    assert response.get_json() == {"error": "uuid parameter missing"}


def test_get_portfolio_controller(client):
    create_response = client.post('/portfolio', json={"value": 1000})

    assert create_response.status_code == 201
    portfolio_id = create_response.get_json()["portfolioId"]

    get_response = client.get(f'/portfolio?portfolioId={portfolio_id}')
    assert get_response.status_code == 200
    assert get_response.get_json() == {
        "portfolioId": portfolio_id,
        "value": 1000
    }
