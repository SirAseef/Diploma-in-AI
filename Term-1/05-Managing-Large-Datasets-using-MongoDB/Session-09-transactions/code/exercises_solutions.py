"""Session 09 - Practice exercise solutions."""
# notebook: run-in-code-dir
import random
from mongo_conn import get_db
from txn import run_transaction


def transfer(db, src, dst, amount):
    def work(session):
        res = db.wallets.update_one({"_id": src, "balance": {"$gte": amount}}, {"$inc": {"balance": -amount}}, session=session)
        if res.modified_count == 0:
            raise ValueError("insufficient")
        db.wallets.update_one({"_id": dst}, {"$inc": {"balance": amount}}, session=session)
    run_transaction(db, work, collections=["wallets"])


if __name__ == "__main__":
    db = get_db("ex09"); db.wallets.drop(); db.students.drop(); db.payments.drop()
    db.wallets.insert_many([{"_id": n, "balance": b, "history": []} for n, b in (("ali", 1000), ("sana", 500), ("omar", 0))])
    db.wallets.update_one({"_id": "ali", "balance": {"$gte": 200}}, {"$inc": {"balance": -200}, "$push": {"history": {"amount": -200}}})
    assert db.wallets.find_one({"_id": "ali"})["balance"] == 800

    total_before = sum(w["balance"] for w in db.wallets.find())
    rng = random.Random(9); failures = 0
    for _ in range(5):
        src, dst = rng.sample(["ali", "sana", "omar"], 2)
        try:
            transfer(db, src, dst, rng.choice([100, 400, 900]))
        except ValueError:
            failures += 1
    assert sum(w["balance"] for w in db.wallets.find()) == total_before
    print("money conserved after 5 transfers;", failures, "failed safely")

    def enrol(session):
        db.students.insert_one({"_id": 11, "name": "New Student"}, session=session)
        raise ValueError("payment gateway timeout")
    try:
        run_transaction(db, enrol, collections=["students", "payments"])
    except ValueError:
        pass
    assert db.students.count_documents({}) == 0
    print("All exercise checks passed")
