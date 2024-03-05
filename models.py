import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_holder = db.Column(db.String(255), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)  
    balance = db.Column(db.Numeric(15, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)  

class Transaction(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  
    account_id = db.Column(db.String(36), db.ForeignKey('account.id'), nullable=False)
    payee = db.Column(db.String(255))
    category = db.Column(db.String(255))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String(50), nullable=False)  
    description = db.Column(db.Text)
