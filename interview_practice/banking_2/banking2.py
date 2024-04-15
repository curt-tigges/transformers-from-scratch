# %%
from dataclasses import dataclass
from typing import Literal, List, Tuple, Optional
from datetime import datetime
import functools
# Level 1

# %%

@dataclass
class User():
    user_id: int
    name: str

@dataclass
class Account():
    account_id: int
    user_id: int
    name: str

@dataclass
class Transaction():
    transaction_id: int
    account_id: int
    type: Literal["deposit", "transfer", "withdrawal"]
    amount: int
    status: Literal["scheduled", "completed", "cancelled"]
    completed_time: Optional[datetime] = None
    scheduled_time: Optional[datetime] = None


class BankingApp():
    def __init__(self):
        self.bank_db = dict()
        self.bank_db["Users"] = dict()
        self.bank_db["Accounts"] = dict()
        self.bank_db["Transactions"] = dict()

        self.user_ids_in_service = {0}
        self.account_ids_in_service = {0}
        self.transaction_ids_in_service = {0}

    def create_user(self, name: str) -> int:
        new_user_id = max(list(self.user_ids_in_service)) + 1
        self.user_ids_in_service.add(new_user_id)
        self.bank_db["Users"][new_user_id] = User(new_user_id, name)
        return new_user_id
    
    def create_account(self, user_id: int, name: str) -> int:
        new_account_id = max(list(self.account_ids_in_service)) + 1
        self.account_ids_in_service.add(new_account_id)
        self.bank_db["Accounts"][new_account_id] = Account(new_account_id, user_id, name)
        return new_account_id
    
    def deposit(self, account_id: int, amount: int, scheduled_time: Optional[datetime]=None) -> int:
        new_transaction_id = max(list(self.transaction_ids_in_service)) + 1
        self.transaction_ids_in_service.add(new_transaction_id)

        if scheduled_time:
            completed_time = None
            status = "scheduled"
        else:
            completed_time = datetime.now()
            status = "completed"

        self.bank_db["Transactions"][new_transaction_id] = Transaction(
            new_transaction_id,
            account_id,
            type="deposit",
            amount=amount,
            status=status,
            completed_time=completed_time,
            scheduled_time=scheduled_time
        )
        return new_transaction_id
    
    def transfer(self, from_account_id: int, to_account_id: int, amount: int, scheduled_time: Optional[datetime]=None) -> List[int]:
        transactions = []
        if scheduled_time:
            completed_time = None
            status = "scheduled"
        else:
            completed_time = datetime.now()
            status = "completed"

        new_transaction_id_from = max(list(self.transaction_ids_in_service)) + 1
        self.transaction_ids_in_service.add(new_transaction_id_from)
        self.bank_db["Transactions"][new_transaction_id_from] = Transaction(
            new_transaction_id_from,
            from_account_id,
            type="transfer",
            amount=-amount,
            status=status,
            completed_time=completed_time,
            scheduled_time=scheduled_time
        )
        transactions.append(new_transaction_id_from)
        new_transaction_id_to = max(self.transaction_ids_in_service) + 1
        self.transaction_ids_in_service.add(new_transaction_id_to)
        self.bank_db["Transactions"][new_transaction_id_to] = Transaction(
            new_transaction_id_to,
            to_account_id,
            type="transfer",
            amount=amount,
            status=status,
            completed_time=completed_time,
            scheduled_time=scheduled_time
        )
        transactions.append(new_transaction_id_to)

        return transactions
    
    def get_user_name(self, user_id: int) -> str:
        return self.bank_db["Users"][user_id].name
    
    def account_exists(self, account_id: int) -> bool:
        return account_id in self.bank_db["Accounts"].keys()

    def get_account_name(self, account_id: int) -> str:
        return self.bank_db["Accounts"][account_id].name

    def get_account_user(self, account_id: int) -> int:
        return self.bank_db["Accounts"][account_id].user_id
    
    def get_transaction_amount(self, transaction_id: int) -> int:
        return self.bank_db["Transactions"][transaction_id].amount
    
    def get_transaction_type(self, transaction_id: int) -> str:
        return self.bank_db["Transactions"][transaction_id].type

    def get_transaction_account(self, transaction_id: int) -> int:
        return self.bank_db["Transactions"][transaction_id].account_id
    
    def get_transaction_status(self, transaction_id: int):
        return self.bank_db["Transactions"][transaction_id].status

    def _get_transaction_totals(self):
        print(self.bank_db)
        transaction_totals = dict()
        for t in self.bank_db["Transactions"].values():
            print(t)
            if t.account_id in transaction_totals.keys():
                transaction_totals[t.account_id] += t.amount
            else:
                transaction_totals[t.account_id] = t.amount
        return transaction_totals
    

    def get_top_accounts(self, k: int) -> List[Tuple[int, int]]:
        totals = self._get_transaction_totals()
        totals = [(k, v) for k, v in totals.items()]
        totals_sorted = sorted(
            totals,
            key=functools.cmp_to_key(lambda a, b: a[1] - b[1]),
            reverse=True
        )
        print(totals_sorted)
        return totals_sorted[:min(k, len(totals_sorted))]
    

        
    def schedule_deposit(self, account_id: int, amount: int, scheduled_time: datetime) -> int:
        return self.deposit(account_id, amount, scheduled_time=scheduled_time)
    
    def schedule_transfer(self, from_account_id: int, to_account_id: int, amount: int, scheduled_time: datetime) -> int:
        return self.transfer(from_account_id, to_account_id, amount, scheduled_time=scheduled_time)[0]
    
    def cancel_transaction(self, transaction_id: int):
        self.bank_db["Transactions"][transaction_id].status="cancelled"
        return True
    
    def perform_scheduled_transactions(self, current_time: datetime):
        performed_transactions = []
        for t in self.bank_db["Transactions"].values():
            print(f"Transaction is: {t}")
            if t.status=="scheduled" and t.scheduled_time <= current_time:
                t.status = "completed"
                t.completed_time = current_time
                performed_transactions.append(t.transaction_id)
        return performed_transactions
    
    def merge_accounts(self, account_id1: int, account_id2: int) -> int:
        for t in self.bank_db["Transactions"].values():
            if t.account_id==account_id2:
                t.account_id=account_id1

        del self.bank_db["Accounts"][account_id2]
        return account_id1
    
    def get_account_balance(self, account_id: int, until: Optional[datetime]=None) -> int:
        
        if not until:
            until = datetime.now()
        
        running_total = 0
        for t in self.bank_db["Transactions"].values():
            if t.status=="completed" and t.completed_time <= until and t.account_id==account_id:
                running_total += t.amount

        return running_total








# %%
