from dataclasses import dataclass, asdict, field
from datetime import datetime, date
from typing import Literal, Optional, List, Tuple
import json


@dataclass
class User():
    user_id: int
    name: str
    email: str
    password: str

@dataclass
class Account():
    account_id: int
    user_id: int
    account_type: Literal["Checking", "Savings"]

@dataclass
class Transaction():
    transaction_id: int
    account_id: int
    transaction_type: Literal["deposit", "withdrawal", "transfer_out", "transfer_in"]
    transaction_status: Literal["pending", "completed", "cancelled"]
    amount: float
    timestamp: str
    scheduled_timestamp: Optional[datetime] = datetime.now()


@dataclass
class Transfer():
    transfer_id: int
    from_account_id: int
    to_account_id: int
    amount: float
    transfer_status: Literal["pending", "completed", "cancelled"]
    transactions: List[int]
    timestamp: str
    scheduled_timestamp: Optional[datetime] = datetime.now()

@dataclass
class Account_History():
    account_id: int
    transactions: Optional[List[int]] = field(default_factory=list)


class Bank():
    def __init__(self) -> None:
        self.users = {}
        self.accounts = {}
        self.transactions = {}
        self.transfers = {}
        self.histories = {}

    def create_user(self, user_id: int, name: str, email: str, password: str):
        if user_id in self.users.keys():
            raise Exception
        self.users[user_id] = User(user_id, name, email, password)

    def create_account(self, account_id: int, user_id: int, account_type: Literal["Checking", "Savings"]):
        if account_id in self.accounts.keys():
            raise Exception
        if user_id not in self.users.keys():
            raise Exception
        self.accounts[account_id] = Account(account_id, user_id, account_type)
        self.histories[account_id] = Account_History(account_id)

    def record_transaction(self, transaction_id: int, account_id: int, transaction_type: Literal["deposit", "withdrawal"], amount: float, timestamp: str):
        if transaction_id in self.transactions.keys():
            raise Exception
        if account_id not in self.accounts.keys():
            raise Exception
        self.transactions[transaction_id] = Transaction(transaction_id, account_id, transaction_type, "completed", amount, timestamp)
        self.histories[account_id].transactions.append(transaction_id)

    def get_account_balance(self, account_id: int):
        if account_id not in self.accounts.keys():
            raise Exception
        
        running_total = 0
        for t in self.transactions.values():
            if t.account_id==account_id:
                if t.transaction_type in ["withdrawal", "transfer_out"]:
                    running_total -= t.amount
                elif t.transaction_type==["deposit", "transfer_in"]:
                    running_total += t.amount
        return running_total

    def get_user_accounts(self, user_id: int) -> List[Account]:
        if user_id not in self.users.keys():
            raise Exception
        accounts = []
        for a in self.accounts.values():
            if a.user_id==user_id:
                accounts.append(a)

        return accounts
    
    def _get_account_totals_abs(self):
        totals = {}

        for t in self.transactions.values():
            if t.account_id in totals.keys():
                totals[t.account_id] += abs(t.amount)
            else:
                totals[t.account_id] = abs(t.amount)
        
        return totals

    def get_top_accounts(self, k: int) -> List[Tuple[int, float]]:
        account_totals = self._get_account_totals_abs()
        totals_list = sorted(
            [(k, v) for k, v in account_totals.items()],
            key=lambda x: (-x[1], x[0])
        )
        return totals_list[:min(k, len(totals_list))]
    
    def _calculate_median(self, sorted_values: List[float]) -> Optional[float]:
        print(sorted_values)
        if len(sorted_values)==1:
            return sorted_values[0]
        elif len(sorted_values)==2:
            return sum(sorted_values) / 2
        else:
            return self._calculate_median(sorted_values[1:-1])

    def get_median_transaction_amount(self) -> Optional[float]:
        amounts = []

        for t in self.transactions.values():
            amounts.append(t.amount)

        amounts.sort()

        return self._calculate_median(amounts)
    
    def filter_transactions_by_type(self, transaction_type: Literal["deposit", "withdrawal"]) -> dict:
        return {k: v for k, v in self.transactions.items() if v.transaction_type==transaction_type}
    
    def aggregate_transactions_by_account(self) -> dict:
        aggregated_transactions = {}

        for t in self.transactions.values():
            if t.account_id in aggregated_transactions:
                aggregated_transactions[t.account_id].append(t)
            else:
                aggregated_transactions[t.account_id] = [t]
        return aggregated_transactions
    
    def export_transactions_to_json(self, account_id: int) -> str:
        transaction_list = [asdict(v) for v in self.transactions.values()]

        return json.dumps(transaction_list)

    def import_transactions_from_json(self, json_data: str) -> None:
        transactions = json.loads(json_data)
        for t in transactions:
            self.transactions[t["transaction_id"]] = Transaction(**t)
            self.histories[t["account_id"]].transactions.append(t["transaction_id"])

    
    # Scheduling capabilities

    def schedule_transaction(
            self, 
            transaction_id: int, 
            account_id: int, 
            transaction_type: Literal["deposit", "withdrawal"],
            amount: float,
            scheduled_timestamp: datetime
        ) -> None:
        if transaction_id in self.transactions.keys():
            raise Exception
        if account_id not in self.accounts.keys():
            raise Exception
        self.transactions[transaction_id] = Transaction(
            transaction_id, account_id, transaction_type, "pending", amount, "", scheduled_timestamp
        )
        self.histories[account_id].transactions.append(transaction_id)

    def cancel_scheduled_transaction(self, transaction_id: int):
        if transaction_id not in self.transactions.keys():
            raise Exception
        if self.transactions[transaction_id].transaction_status=="completed":
            raise Exception
        
        self.transactions[transaction_id].transaction_status = "cancelled"

    def process_scheduled_transactions(self) -> None:
        for t in self.transactions.values():
            if t.scheduled_timestamp <= datetime.now():
                t.transaction_status = "completed"

    def get_new_id(self, table) -> int:
        if len(table) == 0:
            max_transaction_id = -1
        else:
            max_transaction_id = max(set(k for k in table.keys()))
        
        return max_transaction_id + 1

    def transfer_funds(self, from_account_id: int, to_account_id: int, amount: float) -> int:
        
        from_transaction_id = self.get_new_id(self.transactions)
        self.transactions[from_transaction_id] = Transaction(
            from_transaction_id,
            from_account_id,
            "transfer_out",
            "pending",
            amount,
            "",
        )
        self.histories[from_account_id].transactions.append(from_transaction_id)
        
        to_transaction_id = self.get_new_id(self.transactions)
        self.transactions[to_transaction_id] = Transaction(
            to_transaction_id,
            to_account_id,
            "transfer_in",
            "pending",
            amount,
            "",
        )
        self.histories[to_account_id].transactions.append(to_transaction_id)
        
        transfer_id = self.get_new_id(self.transfers)
        self.transfers[transfer_id] = Transfer(
            transfer_id,
            from_account_id,
            to_account_id,
            amount,
            "pending",
            [from_transaction_id, to_transaction_id],
            ""
        )
        
        return transfer_id

    def accept_transfer(self, transfer_id: int):

        transfer = self.transfers[transfer_id]
        transfer.transfer_status = "completed"

        self.transactions[transfer.transactions[0]].transaction_status = "completed"
        self.transactions[transfer.transactions[1]].transaction_status = "completed"

    def merge_accounts(self, from_account_id: int, to_account_id: int) -> None:
        self.histories[to_account_id].transactions = self.histories[from_account_id].transactions + self.histories[to_account_id].transactions

        for tid in self.histories[to_account_id].transactions:
            self.transactions[tid].account_id = to_account_id

        del self.accounts[from_account_id]
        del self.histories[from_account_id]

    def get_account_history(self, account_id: int) -> List:
        return self.histories[account_id].transactions