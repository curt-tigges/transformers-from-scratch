import unittest
from banking2 import BankingApp
import datetime

class TestBankingAppLevel3(unittest.TestCase):

    def setUp(self):
        self.app = BankingApp()

    def test_scheduled_deposit(self):
        user_id = self.app.create_user("John Doe")
        account_id = self.app.create_account(user_id, "Checking")
        future_time = datetime.datetime.now() + datetime.timedelta(days=1)
        transaction_id = self.app.schedule_deposit(account_id, 100, future_time)
        self.assertIsNotNone(transaction_id)
        self.assertEqual(self.app.get_transaction_status(transaction_id), "scheduled")

    def test_scheduled_transfer(self):
        user_id = self.app.create_user("John Doe")
        account_id1 = self.app.create_account(user_id, "Checking")
        account_id2 = self.app.create_account(user_id, "Savings")
        future_time = datetime.datetime.now() + datetime.timedelta(days=1)
        transaction_id = self.app.schedule_transfer(account_id1, account_id2, 50, future_time)
        self.assertIsNotNone(transaction_id)
        self.assertEqual(self.app.get_transaction_status(transaction_id), "scheduled")

    def test_cancel_transaction(self):
        user_id = self.app.create_user("John Doe")
        account_id = self.app.create_account(user_id, "Checking")
        future_time = datetime.datetime.now() + datetime.timedelta(days=1)
        transaction_id = self.app.schedule_deposit(account_id, 100, future_time)
        success = self.app.cancel_transaction(transaction_id)
        self.assertTrue(success)
        self.assertEqual(self.app.get_transaction_status(transaction_id), "cancelled")

    def test_perform_scheduled_transactions(self):
        user_id = self.app.create_user("John Doe")
        account_id = self.app.create_account(user_id, "Checking")
        past_time = datetime.datetime.now() - datetime.timedelta(days=1)
        transaction_id = self.app.schedule_deposit(account_id, 100, past_time)
        completed_transactions = self.app.perform_scheduled_transactions(datetime.datetime.now())
        self.assertIn(transaction_id, completed_transactions)
        self.assertEqual(self.app.get_transaction_status(transaction_id), "completed")

if __name__ == '__main__':
    unittest.main()
