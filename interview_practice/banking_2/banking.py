# %%
from dataclasses import dataclass
from typing import Literal, List, Set, Dict, Optional
from datetime import datetime
import functools

# %%
@dataclass
class User():
    id: int
    name: str
    accounts: Dict


@dataclass
class Account():
    id: int
    user_id: int
    type: Literal["checking", "savings"]
    transactions: Dict


@dataclass
class Transaction():
    amount: int
    account_id: int
    transaction_time: datetime
    completed_time: datetime
    type: Literal["deposit", "transfer", "withdrawal"]
    status: Literal["accepted", "pending"]

db = dict()

# %%
# CRUD

def add_user(user: User) -> int:
    db[user.id] = user

    return 201

def 



# %%
def get_accounts_for_user(user_id: int) -> List[Account]:
    return [a for a in accounts if a.user_id==user_id]


def get_account_balance(account_id: int, until: datetime) -> int:
    return sum(
        t.amount 
        for t in transactions
        if t.account_id == account_id and t.transaction_time <= until
    )

def get_multiple_balances(account_ids: Set[int], until: datetime) -> Dict[int, int]:
    sums = dict()

    for t in transactions:
        if t.account_id in account_ids and t.transaction_time <= until:
            if t.account_id in sums.keys():
                sums[t.account_id] += t.amount
            else:
                sums[t.account_id] = t.amount

    return sums

def get_all_outgoing() -> Dict[int, int]:
    sums = dict()

    for t in transactions:
        if t.amount < 0:
            if t.account_id in sums.keys():
                sums[t.account_id] += t.amount
            else:
                sums[t.account_id] = t.amount
        else:
            if t.account_id in sums.keys():
                sums[t.account_id] += 0
            else:
                sums[t.account_id] = 0

    return sums

def get_topk_outgoing(k: int) -> List[Account]:

    all_outgoing = get_all_outgoing()
    sorted_accounts = sorted(
        accounts, 
        key=functools.cmp_to_key(lambda a, b: all_outgoing.get(a.id, 0) - all_outgoing.get(b.id, 0))
    )
    return sorted_accounts[:k]


def get_all_transactions(account_ids: Set[int]) -> List[Transaction]:
    return [t for t in transactions if t.account_id in account_ids]


def get_median(values: List[int]) -> Optional[int]:

    if len(values):
        return None
    elif len(values) == 1:
        return values[0]
    elif len(values) == 2:
        return sum(values) // 2
    else:
        return get_median(values[1:-1])
        


def get_median_transaction_value(user_id: int, type: Literal["credit", "debit", "all"]) -> Optional[int]:
    user_account_ids = {a.id for a in accounts if a.user_id==user_id}
    user_transactions = get_all_transactions(user_account_ids)

    if type=="credit":
        return get_median([t.amount for t in user_transactions if t.amount>=0])
    elif type=="debit":
        return get_median([t.amount for t in user_transactions if t.amount<0])
    elif type=="all":
        return get_median([t.amount for t in user_transactions])

# %%
test_user = User(id=1, name="bob")
#test_account = Account(type="checking")

users = [User(id=i, name=f"user_{i}") for i in range(5)]
accounts = [
    Account(id=0, user_id=0, type="savings"),
    Account(id=1, user_id=0, type="checking"),
    Account(id=2, user_id=1, type="savings"),
    Account(id=3, user_id=1, type="checking"),
    Account(id=4, user_id=4, type="checking"),
    ]

transactions = [
    Transaction(amount=294, account_id=0, transaction_time=datetime.now(), source="external"),
    Transaction(amount=1500, account_id=1, transaction_time=datetime.now(), source="external"),
    Transaction(amount=-100, account_id=2, transaction_time=datetime.now(), source="external"),
    Transaction(amount=-250, account_id=4, transaction_time=datetime.now(), source="external"),
    Transaction(amount=-433, account_id=3, transaction_time=datetime.now(), source="external"),
    Transaction(amount=2000, account_id=0, transaction_time=datetime.now(), source="external"),
    ]




accts = get_accounts_for_user(user_id=0)
print(accts)


print(f"Balance for account {0}: {get_account_balance(account_id=0, until=datetime.now())}")

print(f"Balances for accounts: {get_multiple_balances(account_ids={0,1}, until=datetime.now())}")

print(f"Top 3 accounts by outgoing: {get_topk_outgoing(3)}")

print(f"Median transaction value for {0}: {get_median_transaction_value(user_id=0, type='all')}")
#test_it = Transaction(amount=500, account_id=1, source="external")
# %%
