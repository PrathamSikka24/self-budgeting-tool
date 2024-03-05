from flask import Flask, request, jsonify
from models import db, Account, Transaction  
import uuid
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'  # I will add this
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/accounts', methods=['POST'])
def add_account():
    pass

@app.route('/accounts', methods=['GET'])
def get_accounts():
    pass
    
if __name__ == "__main__":
    app.run(debug=True)
