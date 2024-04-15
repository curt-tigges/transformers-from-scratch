import unittest
from banking_app import Bank

class TestBankingApp(unittest.TestCase):
    def setUp(self):
        # Clear the dictionaries before each test
        self.app = Bank()

    def test_create_user(self):
        self.app.create_user(1, "John Doe", "john@example.com", "password123")
        user = self.app.users[1]
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertEqual(user.password, "password123")

    # def test_create_user_invalid_data(self):
    #     with self.assertRaises(TypeError):
    #         self.app.create_user(1, 123, "john@example.com", "password123")
        #with self.assertRaises(ValueError):
        #    self.app.create_user(1, "John Doe", "invalid_email", "password123")

    def test_create_user_duplicate_id(self):
        self.app.create_user(1, "John Doe", "john@example.com", "password123")
        with self.assertRaises(Exception):
            self.app.create_user(1, "Jane Smith", "jane@example.com", "password456")

    def test_create_account(self):
        self.app.create_user(1, "John Doe", "john@example.com", "password123")
        self.app.create_account(1, 1, "Checking")
        account = self.app.accounts[1]
        self.assertEqual(account.account_id, 1)
        self.assertEqual(account.user_id, 1)
        self.assertEqual(account.account_type, "Checking")

    # def test_create_account_invalid_data(self):
    #     self.app.create_user(1, "John Doe", "john@example.com", "password123")
    #     with self.assertRaises(TypeError):
    #         self.app.create_account("invalid_id", 1, "Checking")
    #     with self.assertRaises(TypeError):
    #         self.app.create_account(1, 1, 123)

    def test_create_account_duplicate_id(self):
        self.app.create_user(1, "John Doe", "john@example.com", "password123")
        self.app.create_account(1, 1, "Checking")
        with self.assertRaises(Exception):
            self.app.create_account(1, 1, "Savings")

    def test_create_account_invalid_user(self):
        with self.assertRaises(Exception):
            self.app.create_account(1, 1, "Checking")

    def test_record_transaction(self):
        self.app.create_user(1, "John Doe", "john@example.com", "password123")
        self.app.create_account(1, 1, "Checking")
        self.app.record_transaction(1, 1, "deposit", 1000, "2023-06-01")
        transaction = self.app.transactions[1]
        self.assertEqual(transaction.transaction_id, 1)
        self.assertEqual(transaction.account_id, 1)
        self.assertEqual(transaction.transaction_type, "deposit")
        self.assertEqual(transaction.amount, 1000)
        self.assertEqual(transaction.timestamp, "2023-06-01")

    # def test_record_transaction_invalid_data(self):
    #     self.app.create_user(1, "John Doe", "john@example.com", "password123")
    #     self.app.create_account(1, 1, "Checking")
    #     with self.assertRaises(TypeError):
    #         self.app.record_transaction("invalid_id", 1, "deposit", 1000, "2023-06-01")
    #     with self.assertRaises(TypeError):
    #         self.app.record_transaction(1, 1, "invalid_type", 1000, "2023-06-01")
    #     with self.assertRaises(TypeError):
    #         self.app.record_transaction(1, 1, "deposit", "invalid_amount", "2023-06-01")

    def test_record_transaction_invalid_account(self):
        with self.assertRaises(Exception):
            self.app.record_transaction(1, 1, "deposit", 1000, "2023-06-01")

    def test_get_account_balance(self):
        self.app.create_user(1, "John Doe", "john@example.com", "password123")
        self.app.create_account(1, 1, "Checking")
        self.app.record_transaction(1, 1, "deposit", 1000, "2023-06-01")
        self.app.record_transaction(2, 1, "withdrawal", 500, "2023-06-02")
        balance = self.app.get_account_balance(1)
        self.assertEqual(balance, 500)

    def test_get_account_balance_invalid_account(self):
        with self.assertRaises(Exception):
            self.app.get_account_balance(1)

    def test_get_user_accounts(self):
        self.app.create_user(1, "John Doe", "john@example.com", "password123")
        self.app.create_account(1, 1, "Checking")
        self.app.create_account(2, 1, "Savings")
        user_accounts = self.app.get_user_accounts(1)
        self.assertEqual(len(user_accounts), 2)
        self.assertEqual(user_accounts[0].account_id, 1)
        self.assertEqual(user_accounts[1].account_id, 2)

    def test_get_user_accounts_invalid_user(self):
        with self.assertRaises(Exception):
            self.app.get_user_accounts(1)

if __name__ == '__main__':
    unittest.main()