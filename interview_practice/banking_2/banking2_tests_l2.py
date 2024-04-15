import unittest
from banking2 import BankingApp

class TestBankingAppLevel2(unittest.TestCase):

    def setUp(self):
        self.app = BankingApp()

    def test_get_top_accounts(self):
        user_id = self.app.create_user("John Doe")
        account_id1 = self.app.create_account(user_id, "Checking")
        account_id2 = self.app.create_account(user_id, "Savings")
        account_id3 = self.app.create_account(user_id, "Investment")

        self.app.deposit(account_id1, 100)
        self.app.deposit(account_id2, 200)
        self.app.deposit(account_id3, 300)

        top_accounts = self.app.get_top_accounts(2)
        self.assertEqual(len(top_accounts), 2)
        self.assertEqual(top_accounts[0], (account_id3, 300))
        self.assertEqual(top_accounts[1], (account_id2, 200))

        # Test with k greater than the number of accounts
        top_accounts_all = self.app.get_top_accounts(5)
        self.assertEqual(len(top_accounts_all), 3)
        self.assertEqual(top_accounts_all[0], (account_id3, 300))
        self.assertEqual(top_accounts_all[1], (account_id2, 200))
        self.assertEqual(top_accounts_all[2], (account_id1, 100))

if __name__ == '__main__':
    unittest.main()
