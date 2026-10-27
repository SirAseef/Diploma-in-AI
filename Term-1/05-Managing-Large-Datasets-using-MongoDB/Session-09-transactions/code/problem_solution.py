"""Session 09 - Real-life problem: canteen purchase as one all-or-nothing transaction."""
# notebook: run-in-code-dir
from mongo_conn import get_db
from txn import run_transaction


def buy_meal(db, student, items):
    def work(session):
        total = 0
        for item, qty in items.items():
            res = db.menu.find_one_and_update({"_id": item, "stock": {"$gte": qty}},
                                              {"$inc": {"stock": -qty}}, session=session)
            if res is None:
                raise ValueError(f"{item} out of stock")
            total += res["price"] * qty
        res = db.wallets.update_one({"_id": student, "balance": {"$gte": total}},
                                    {"$inc": {"balance": -total}}, session=session)
        if res.modified_count == 0:
            raise ValueError("insufficient balance")
        db.receipts.insert_one({"student": student, "items": items, "total": total}, session=session)
        return total
    return run_transaction(db, work, collections=["menu", "wallets", "receipts"])


def state(db):
    return ({m["_id"]: m["stock"] for m in db.menu.find()}, {w["_id"]: w["balance"] for w in db.wallets.find()},
            db.receipts.count_documents({}))


if __name__ == "__main__":
    db = get_db("canteen_demo")
    for c in ("menu", "wallets", "receipts"):
        db[c].drop()
    db.menu.insert_many([{"_id": "biryani", "price": 250, "stock": 10}, {"_id": "samosa", "price": 40, "stock": 2},
                         {"_id": "chai", "price": 60, "stock": 50}])
    db.wallets.insert_many([{"_id": "ali", "balance": 1000}, {"_id": "hamza", "balance": 200}])

    total = buy_meal(db, "ali", {"biryani": 2, "chai": 1})
    print("ali paid", total, "->", state(db))
    assert total == 560 and state(db) == ({"biryani": 8, "samosa": 2, "chai": 49}, {"ali": 440, "hamza": 200}, 1)

    before = state(db)
    for student, order in (("ali", {"chai": 1, "samosa": 3}), ("hamza", {"biryani": 1})):
        try:
            buy_meal(db, student, order)
        except ValueError as e:
            print(student, "failed:", e)
        assert state(db) == before, "a failed purchase must change nothing"
    print("All checks passed")
