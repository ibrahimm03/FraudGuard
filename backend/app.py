from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime
import sys
import os
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import (
    create_tables,
    add_card,
    add_transaction,
    get_all_transactions,
    get_recent_transactions,
    flag_transaction,
    create_alert,
    get_all_alerts
)
from fraud_engine import FraudEngine

engine = FraudEngine()

# Tell Flask where the frontend files live
frontend_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')
app = Flask(__name__, static_folder=frontend_folder)

create_tables()

# Serve the frontend
@app.route('/')
def index():
    return send_from_directory(frontend_folder, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(frontend_folder, filename)

# -------------------------
# TRANSACTION ENDPOINTS
# -------------------------

@app.route('/transactions', methods=['GET'])
def get_transactions():
    """Return all transactions"""
    transactions = get_all_transactions()
    return jsonify(transactions)

@app.route('/transactions', methods=['POST'])
def new_transaction():
    """Add a new transaction and analyse it for fraud"""
    data = request.get_json()
    transaction_id = add_transaction(
        card_number=data['card_number'],
        amount=data['amount'],
        merchant=data['merchant'],
        location=data['location'],
        timestamp=datetime.now().isoformat()
    )

    alerts = engine.analyse(
        transaction_id=transaction_id,
        card_number=data['card_number'],
        amount=data['amount'],
        location=data['location'],
        timestamp=datetime.now().isoformat()
    )

    return jsonify({
        'id': transaction_id,
        'message': 'Transaction added',
        'alerts': alerts
    }), 201

@app.route('/transactions/<int:transaction_id>/flag', methods=['PUT'])
def flag(transaction_id):
    """Flag a transaction as fraudulent"""
    flag_transaction(transaction_id)
    return jsonify({'message': 'Transaction flagged as fraudulent'})

# -------------------------
# ALERT ENDPOINTS
# -------------------------

@app.route('/alerts', methods=['GET'])
def get_alerts():
    """Return all alerts"""
    alerts = get_all_alerts()
    return jsonify(alerts)

# -------------------------
# CARD ENDPOINTS
# -------------------------

@app.route('/cards', methods=['POST'])
def new_card():
    """Add a new card"""
    data = request.get_json()
    add_card(
        card_number=data['card_number'],
        cardholder_name=data['cardholder_name'],
        daily_limit=data['daily_limit']
    )
    return jsonify({'message': 'Card added'}), 201

# -------------------------
# RUN THE SERVER
# -------------------------

if __name__ == '__main__':
    app.run(debug=True)