import unittest
from banking2 import BankingApp

class TestBankingAppLevel1(unittest.TestCase):

    def setUp(self):
        self.app = BankingApp()

    def test_user_creation(self):
        user_id = self.app.create_user("John Doe")
        self.assertIsNotNone(user_id)
        self.assertEqual(self.app.get_user_name(user_id), "John Doe")

    def test_account_creation(self):
        user_id = self.app.create_user("John Doe")
        account_id = self.app.create_account(user_id, "Checking")
        self.assertIsNotNone(account_id)
        self.assertEqual(self.app.get_account_name(account_id), "Checking")
        self.assertEqual(self.app.get_account_user(account_id), user_id)

    def test_deposit(self):
        user_id = self.app.create_user("John Doe")
        account_id = self.app.create_account(user_id, "Checking")
        transaction_id = self.app.deposit(account_id, 100)
        self.assertIsNotNone(transaction_id)
        self.assertEqual(self.app.get_transaction_amount(transaction_id), 100)
        self.assertEqual(self.app.get_transaction_type(transaction_id), "deposit")

    def test_transfer(self):
        user_id = self.app.create_user("John Doe")
        account_id1 = self.app.create_account(user_id, "Checking")
        account_id2 = self.app.create_account(user_id, "Savings")
        transaction_ids = self.app.transfer(account_id1, account_id2, 50)
        self.assertEqual(len(transaction_ids), 2)

        withdrawal_transaction_id, deposit_transaction_id = transaction_ids

        # Check the withdrawal transaction
        self.assertEqual(self.app.get_transaction_amount(withdrawal_transaction_id), -50)
        self.assertEqual(self.app.get_transaction_type(withdrawal_transaction_id), "transfer")
        self.assertEqual(self.app.get_transaction_account(withdrawal_transaction_id), account_id1)

        # Check the deposit transaction
        self.assertEqual(self.app.get_transaction_amount(deposit_transaction_id), 50)
        self.assertEqual(self.app.get_transaction_type(deposit_transaction_id), "transfer")
        self.assertEqual(self.app.get_transaction_account(deposit_transaction_id), account_id2)


if __name__ == '__main__':
    unittest.main()