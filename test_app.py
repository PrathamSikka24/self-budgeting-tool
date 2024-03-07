import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('mysql.connector.connect')
    def test_get_accounts(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"id": 1, "name": "Account 1", "balance": 1000},
            {"id": 2, "name": "Account 2", "balance": 2000},
        ]
        mock_connect.return_value.cursor.return_value = mock_cursor

        response = self.app.get('/accounts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"data": mock_cursor.fetchall.return_value})

    @patch('mysql.connector.connect')
    def test_get_transactions(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"id": 1, "account_id": 1, "payee": "Netflix", "amount": -15, "category": "Entertainment"},
            {"id": 2, "account_id": 2, "payee": "Grocery Store", "amount": -100, "category": "Groceries"},
        ]
        mock_connect.return_value.cursor.return_value = mock_cursor

        response = self.app.get('/transactions')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"data": mock_cursor.fetchall.return_value})

    @patch('mysql.connector.connect')
    def test_add_transaction(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = None
        transaction_data = {
            "account_id": "1",
            "bank_name": "Test Bank",
            "date": "2022-01-01",
            "type": "debit",
            "payee": "New Payee",
            "amount": 50,
            "category": "Test Category",
        }
        
        response = self.app.post('/transactions', json=transaction_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Transaction added successfully"})

        mock_cursor.execute.assert_called_once()
        mock_connect.return_value.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
