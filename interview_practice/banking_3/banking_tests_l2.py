import unittest
import json
from banking_app import Bank

class TestBankingAppLevel2(unittest.TestCase):
    def setUp(self):
        # Create a new instance of the Bank class before each test
        self.app = Bank()

    def test_get_top_accounts(self):
        self.app.create_user(1, "John Doe", "john@example.com", "password123")
        self.app.create_account(1, 1, "Checking")
        self.app.create_account(2, 1, "Savings")
        self.app.record_transaction(1, 1, "deposit", 1000, "2023-06-01")
        self.app.record_transaction(2, 1, "withdrawal", 500, "2023-06-02")
        self.app.record_transaction(3, 2, "deposit", 2000, "2023-06-03")
        self.app.record_transaction(4, 2, "withdrawal", 800, "2023-06-04")

        top_accounts = self.app.get_top_accounts(2)
        self.assertEqual(len(top_accounts), 2)
        self.assertEqual(top_accounts[0], (2, 2800))
        self.assertEqual(top_accounts[1], (1, 1500))

    def test_get_median_transaction_amount(self):
        self.app.create_user(1, "John Doe", "john@example.com", "password123")
        self.app.create_account(1, 1, "Checking")
        self.app.create_account(2, 1, "Savings")
        self.app.record_transaction(1, 1, "deposit", 1000, "2023-06-01")
        self.app.record_transaction(2, 1, "withdrawal", 500, "2023-06-02")
        self.app.record_transaction(3, 2, "deposit", 2000, "2023-06-03")
        self.app.record_transaction(4, 2, "withdrawal", 800, "2023-06-04")

        median_amount = self.app.get_median_transaction_amount()
        self.assertEqual(median_amount, 900)

    def test_filter_transactions_by_type(self):
        self.app.create_user(1, "John Doe", "john@example.com", "password123")
        self.app.create_account(1, 1, "Checking")
        self.app.create_account(2, 1, "Savings")
        self.app.record_transaction(1, 1, "deposit", 1000, "2023-06-01")
        self.app.record_transaction(2, 1, "withdrawal", 500, "2023-06-02")
        self.app.record_transaction(3, 2, "deposit", 2000, "2023-06-03")
        self.app.record_transaction(4, 2, "withdrawal", 800, "2023-06-04")

        deposit_transactions = self.app.filter_transactions_by_type("deposit")
        self.assertEqual(len(deposit_transactions), 2)
        self.assertIn(1, deposit_transactions)
        self.assertIn(3, deposit_transactions)

    def test_aggregate_transactions_by_account(self):
        self.app.create_user(1, "John Doe", "john@example.com", "password123")
        self.app.create_account(1, 1, "Checking")
        self.app.create_account(2, 1, "Savings")
        self.app.record_transaction(1, 1, "deposit", 1000, "2023-06-01")
        self.app.record_transaction(2, 1, "withdrawal", 500, "2023-06-02")
        self.app.record_transaction(3, 2, "deposit", 2000, "2023-06-03")
        self.app.record_transaction(4, 2, "withdrawal", 800, "2023-06-04")

        aggregated_transactions = self.app.aggregate_transactions_by_account()
        self.assertEqual(len(aggregated_transactions), 2)
        self.assertEqual(len(aggregated_transactions[1]), 2)
        self.assertEqual(len(aggregated_transactions[2]), 2)

    def test_export_transactions_to_json(self):
        self.app.create_user(1, "John Doe", "john@example.com", "password123")
        self.app.create_account(1, 1, "Checking")
        self.app.record_transaction(1, 1, "deposit", 1000, "2023-06-01")
        self.app.record_transaction(2, 1, "withdrawal", 500, "2023-06-02")

        json_data = self.app.export_transactions_to_json(1)
        expected_json = '[{"transaction_id": 1, "account_id": 1, "transaction_type": "deposit", "amount": 1000, "timestamp": "2023-06-01"}, {"transaction_id": 2, "account_id": 1, "transaction_type": "withdrawal", "amount": 500, "timestamp": "2023-06-02"}]'
        self.assertEqual(json.loads(json_data), json.loads(expected_json))

    def test_import_transactions_from_json(self):
        self.app.create_user(1, "John Doe", "john@example.com", "password123")
        self.app.create_account(1, 1, "Checking")
        self.app.create_account(2, 1, "Savings")
        self.app.record_transaction(1, 1, "deposit", 1000, "2023-06-01")
        self.app.record_transaction(2, 1, "withdrawal", 500, "2023-06-02")
        self.app.record_transaction(3, 2, "deposit", 2000, "2023-06-03")
        self.app.record_transaction(4, 2, "withdrawal", 800, "2023-06-04")

        json_data = '[{"transaction_id": 5, "account_id": 1, "transaction_type": "deposit", "amount": 1500, "timestamp": "2023-06-05"}, {"transaction_id": 6, "account_id": 2, "transaction_type": "withdrawal", "amount": 1000, "timestamp": "2023-06-06"}]'
        self.app.import_transactions_from_json(json_data)
        self.assertEqual(len(self.app.transactions), 6)
        self.assertEqual(self.app.transactions[5].transaction_id, 5)
        self.assertEqual(self.app.transactions[6].transaction_id, 6)

    # def test_import_transactions_from_json_invalid_data(self):
    #     self.app.create_user(1, "John Doe", "john@example.com", "password123")
    #     self.app.create_account(1, 1, "Checking")
    #     self.app.create_account(2, 1, "Savings")

    #     json_data = '[{"transaction_id": 5, "account_id": 1, "transaction_type": "invalid", "amount": 1500, "timestamp": "2023-06-05"}]'
    #     with self.assertRaises(ValueError):
    #         self.app.import_transactions_from_json(json_data)

if __name__ == '__main__':
    unittest.main()