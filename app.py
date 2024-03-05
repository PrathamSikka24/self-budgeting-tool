from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_DATABASE'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

@app.route('/accounts', methods=['GET'])
def get_accounts():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM accounts')
        accounts = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(accounts)
    else:
        return jsonify({"error": "Database connection failed"}), 500

@app.route('/transactions', methods=['GET'])
def get_transactions():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)  # Use `dictionary=True` to get results as dictionaries
        cursor.execute('SELECT * FROM transactions')
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(transactions)
    else:
        return jsonify({"error": "Database connection failed"}), 500

@app.route('/transactions', methods=['POST'])
def add_transaction():
    transaction_data = request.json
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO transactions (account_id, payee, amount, category) VALUES (%s, %s, %s, %s)',
                       (transaction_data['account_id'], transaction_data['payee'], transaction_data['amount'], transaction_data['category']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Transaction added successfully"}), 201
    else:
        return jsonify({"error": "Database connection failed"}), 500

if __name__ == "__main__":
    app.run(debug=True)
