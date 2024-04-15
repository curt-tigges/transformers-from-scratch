import unittest
from datetime import datetime, timedelta
from banking_app import Bank

class TestBankingAppLevel4(unittest.TestCase):
    def setUp(self):
        self.app = Bank()
        self.app.create_user(1, "John Doe", "john@example.com", "password123")
        self.app.create_account(1, 1, "Checking")
        self.app.create_account(2, 1, "Savings")
        self.app.record_transaction(1, 1, "deposit", 1000, "2023-06-01")
        self.app.record_transaction(2, 1, "withdrawal", 500, "2023-06-02")
        self.app.record_transaction(3, 2, "deposit", 2000, "2023-06-03")
        self.app.record_transaction(4, 2, "withdrawal", 800, "2023-06-04")

    def test_get_account_history(self):
        account_history = self.app.get_account_history(1)
        self.assertEqual(len(account_history), 2)
        self.assertIn(1, account_history)
        self.assertIn(2, account_history)

    def test_merge_accounts(self):
        self.app.merge_accounts(1, 2)
        self.assertNotIn(1, self.app.accounts)
        self.assertNotIn(1, self.app.histories)
        account_history = self.app.get_account_history(2)
        self.assertEqual(len(account_history), 4)
        for transaction_id in account_history:
            transaction = self.app.transactions[transaction_id]
            self.assertEqual(transaction.account_id, 2)

    def test_merge_accounts_invalid(self):
        with self.assertRaises(Exception):
            self.app.merge_accounts(1, 3)

if __name__ == '__main__':
    unittest.main()