from flask import Flask, jsonify, request
from adapters.persistence.In_memory_portfolio_repository import InMemoryPortfolioRepository
from domain.Portfolio import Portfolio
import uuid

app = Flask(__name__)
repo = InMemoryPortfolioRepository()

@app.route('/portfolio', methods=['GET'])
def get_portfolio():
    portfolio_id_str = request.args.get('portfolioId')
    if not portfolio_id_str:
        return jsonify({"error": "uuid parameter missing"}), 400

    try:
        portfolio_id = uuid.UUID(portfolio_id_str)
    except ValueError:
        return jsonify({"error": "invalid uuid format"}), 400

    portfolio = repo.get_portfolio(portfolio_id)
    if portfolio is None:
        return jsonify({"error": "portfolio not found"}), 404

    return jsonify({"portfolioId": str(portfolio.portfolio_id), "value": portfolio.value}), 200

@app.route('/portfolio', methods=['POST'])
def create_portfolio():
    data = request.get_json()
    value = data.get('value') if data else None
    if not value:
        return jsonify({"error": "value parameter missing"}), 400

    portfolio = Portfolio.create(value)
    repo.save_portfolio(portfolio)

    return jsonify({
        "success": "portfolio is added",
        "portfolioId": str(portfolio.portfolio_id),
        "portfolioValue": portfolio.value
    }), 201

if __name__ == '__main__':
    app.run(port=8000)