"""Session 09 - Transactions: worked examples (emulated rollback on mongomock, real transactions on a replica set)."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Setup: wallets

# %%
from mongo_conn import get_db
from txn import run_transaction
db = get_db("campus_txn")
db.wallets.drop(); db.stock.drop(); db.orders.drop()
db.wallets.insert_many([{"_id": "ali", "balance": 5000, "history": []}, {"_id": "sana", "balance": 20000, "history": []},
                        {"_id": "hamza", "balance": 3000, "history": []}, {"_id": "fees", "balance": 0, "history": []}])

def balances():
    return {w["_id"]: w["balance"] for w in db.wallets.find()}

def debit(db, who, amount, session=None):
    res = db.wallets.update_one({"_id": who, "balance": {"$gte": amount}}, {"$inc": {"balance": -amount}}, session=session)
    if res.modified_count == 0:
        raise ValueError(f"{who}: insufficient balance")

def credit(db, who, amount, session=None):
    db.wallets.update_one({"_id": who}, {"$inc": {"balance": amount}}, session=session)

print(balances())

# %% [markdown]
# ## Example 1 - single-document atomicity

# %%
db.wallets.update_one({"_id": "ali"}, {"$inc": {"balance": -500}, "$push": {"history": {"type": "canteen", "amount": -500}}})
print(db.wallets.find_one({"_id": "ali"}))

# %% [markdown]
# ## Example 2 - the problem without a transaction

# %%
try:
    debit(db, "sana", 15000)
    raise RuntimeError("power cut!")
except RuntimeError as e:
    print(e, "->", balances(), "| total:", sum(balances().values()))
credit(db, "sana", 15000)                  # undo by hand for the next example

# %% [markdown]
# ## Example 3 - a transfer inside a transaction

# %%
def transfer(session):
    debit(db, "sana", 15000, session); credit(db, "fees", 15000, session)

run_transaction(db, transfer, collections=["wallets"])
print(balances())
assert balances()["fees"] == 15000

# %% [markdown]
# ## Example 4 - automatic rollback

# %%
def bad_transfer(session):
    credit(db, "fees", 50000, session)     # applied first ...
    debit(db, "hamza", 50000, session)     # ... then this fails
before = balances()
try:
    run_transaction(db, bad_transfer, collections=["wallets"])
except ValueError as e:
    print("aborted:", e)
print(balances())
assert balances() == before

# %% [markdown]
# ## Example 5 - order + stock in two collections

# %%
db.stock.insert_one({"_id": "laptop", "qty": 1})

def place_order(session, student):
    res = db.stock.update_one({"_id": "laptop", "qty": {"$gte": 1}}, {"$inc": {"qty": -1}}, session=session)
    if res.modified_count == 0:
        raise ValueError("out of stock")
    db.orders.insert_one({"item": "laptop", "student": student}, session=session)

for student in ("faraz", "zoya"):
    try:
        run_transaction(db, lambda s: place_order(s, student), collections=["stock", "orders"])
        print(student, "-> order placed")
    except ValueError as e:
        print(student, "->", e)
print("stock:", db.stock.find_one()["qty"], "| orders:", db.orders.count_documents({}))

# %% [markdown]
# ## Example 6 - design instead of a transaction

# %%
db.wallets.update_one({"_id": "ali"}, {"$inc": {"balance": 1000}, "$push": {"history": {"type": "top-up", "amount": 1000}}})
print(db.wallets.find_one({"_id": "ali"}, {"_id": 0}))
