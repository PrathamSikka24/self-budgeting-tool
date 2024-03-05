from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Routes
@app.route('/accounts', methods=['POST'])
def add_account():
    data = request.get_json()
    new_account = Account(
        account_number=data['account_number'],
        account_holder=data['account_holder'],
        account_type=data['account_type'],
        balance=data['balance']
    )
    db.session.add(new_account)
    db.session.commit()
    return jsonify({'message': 'Account created successfully'}), 201

@app.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = Account.query.all()
    output = []
    for account in accounts:
        account_data = {
            'id': account.id,
            'account_number': account.account_number,
            'account_holder': account.account_holder,
            'account_type': account.account_type,
            'balance': str(account.balance)  # Convert Decimal to string for JSON serialization
        }
        output.append(account_data)
    return jsonify({'accounts': output}), 200

@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    new_transaction = Transaction(
        account_id=data['account_id'],
        payee=data['payee'],
        category=data['category'],
        amount=data['amount'],
        type=data['type'],
        description=data.get('description', '')
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction recorded successfully'}), 201

@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    output = []
    for transaction in transactions:
        transaction_data = {
            'id': transaction.id,
            'date': transaction.date.isoformat(),
            'account_id': transaction.account_id,
            'payee': transaction.payee,
            'category': transaction.category,
            'amount': str(transaction.amount),
            'type': transaction.type,
            'description': transaction.description
        }
        output.append(transaction_data)
    return jsonify({'transactions': output}), 200


if __name__ == "__main__":
    from models import *  
    db.create_all()  
    app.run(debug=True)
