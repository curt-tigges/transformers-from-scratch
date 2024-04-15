import unittest
from banking2 import BankingApp
from datetime import datetime

class TestBankingAppLevel4(unittest.TestCase):

    def setUp(self):
        self.app = BankingApp()

    def test_merge_accounts(self):
        user_id = self.app.create_user("John Doe")
        account_id1 = self.app.create_account(user_id, "Checking")
        account_id2 = self.app.create_account(user_id, "Savings")

        self.app.deposit(account_id1, 100)
        self.app.deposit(account_id2, 200)

        merged_account_id = self.app.merge_accounts(account_id1, account_id2)
        self.assertEqual(merged_account_id, account_id1)

        # Check that the transaction history of both accounts is now in the merged account
        self.assertEqual(self.app.get_account_balance(merged_account_id), 300)
        self.assertFalse(self.app.account_exists(account_id2))

if __name__ == '__main__':
    unittest.main()