from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/accounts', methods=['POST'])
def add_account():
    # Implementation of adding an account
    pass

@app.route('/accounts', methods=['GET'])
def get_accounts():
    # Implementation of fetching accounts
    pass

if __name__ == "__main__":
    from models import *  
    db.create_all()  
    app.run(debug=True)
