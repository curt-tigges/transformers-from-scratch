import unittest
from datetime import datetime, timedelta
from banking_app import Bank
from time import sleep

class TestBankingAppLevel3(unittest.TestCase):
    def setUp(self):
        self.app = Bank()
        self.app.create_user(1, "John Doe", "john@example.com", "password123")
        self.app.create_account(1, 1, "Checking")
        self.app.create_account(2, 1, "Savings")

    def test_schedule_transaction(self):
        scheduled_timestamp = datetime.now() + timedelta(days=1)
        self.app.schedule_transaction(1, 1, "deposit", 1000, scheduled_timestamp)
        transaction = self.app.transactions[1]
        self.assertEqual(transaction.transaction_status, "pending")
        self.assertEqual(transaction.scheduled_timestamp, scheduled_timestamp)

    def test_cancel_scheduled_transaction(self):
        scheduled_timestamp = datetime.now() + timedelta(days=1)
        self.app.schedule_transaction(1, 1, "deposit", 1000, scheduled_timestamp)
        self.app.cancel_scheduled_transaction(1)
        transaction = self.app.transactions[1]
        self.assertEqual(transaction.transaction_status, "cancelled")

    def test_process_scheduled_transactions(self):
        scheduled_timestamp = datetime.now() + timedelta(seconds=1)
        self.app.schedule_transaction(1, 1, "deposit", 1000, scheduled_timestamp)
        self.app.schedule_transaction(2, 2, "withdrawal", 500, scheduled_timestamp)
        sleep(1)
        self.app.process_scheduled_transactions()
        transaction1 = self.app.transactions[1]
        transaction2 = self.app.transactions[2]
        self.assertEqual(transaction1.transaction_status, "completed")
        self.assertEqual(transaction2.transaction_status, "completed")

    def test_transfer_funds(self):
        transfer_id = self.app.transfer_funds(1, 2, 1000)
        transfer = self.app.transfers[transfer_id]
        self.assertEqual(transfer.from_account_id, 1)
        self.assertEqual(transfer.to_account_id, 2)
        self.assertEqual(transfer.amount, 1000)
        self.assertEqual(transfer.transfer_status, "pending")
        self.assertEqual(len(transfer.transactions), 2)
        transaction_out = self.app.transactions[transfer.transactions[0]]
        transaction_in = self.app.transactions[transfer.transactions[1]]
        self.assertEqual(transaction_out.transaction_type, "transfer_out")
        self.assertEqual(transaction_out.account_id, 1)
        self.assertEqual(transaction_out.amount, 1000)
        self.assertEqual(transaction_in.transaction_type, "transfer_in")
        self.assertEqual(transaction_in.account_id, 2)
        self.assertEqual(transaction_in.amount, 1000)

    def test_accept_transfer(self):
        transfer_id = self.app.transfer_funds(1, 2, 1000)
        self.app.accept_transfer(transfer_id)
        transfer = self.app.transfers[transfer_id]
        self.assertEqual(transfer.transfer_status, "completed")
        transaction_out = self.app.transactions[transfer.transactions[0]]
        transaction_in = self.app.transactions[transfer.transactions[1]]
        self.assertEqual(transaction_out.transaction_status, "completed")
        self.assertEqual(transaction_in.transaction_status, "completed")

    def test_accept_invalid_transfer(self):
        with self.assertRaises(Exception):
            self.app.accept_transfer(1)

if __name__ == '__main__':
    unittest.main()