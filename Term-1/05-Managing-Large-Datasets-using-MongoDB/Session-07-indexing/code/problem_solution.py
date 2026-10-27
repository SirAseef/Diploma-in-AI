"""Session 07 - Real-life problem: index design for an e-commerce orders collection."""
# notebook: run-in-code-dir
import random
from datetime import datetime, timedelta
from pymongo.errors import DuplicateKeyError
from index_sim import build_index, collscan, ixscan
from mongo_conn import get_db

INDEXES = {
    "customer_newest": [("customer_id", 1), ("created_at", -1)],
    "status_city_date": [("status", 1), ("city", 1), ("created_at", -1)],
    "order_no_unique": [("order_no", 1)],
}


def create_indexes(db):
    for name, keys in INDEXES.items():
        db.orders.create_index(keys, name=name, unique=(name == "order_no_unique"))
    return sorted(db.orders.index_information())


def compare_lookup(docs, order_no):
    scan = collscan(docs, "order_no", order_no)
    seek = ixscan(build_index(docs, "order_no"), order_no)
    return scan["examined"], seek["examined"]


if __name__ == "__main__":
    rng = random.Random(77)
    start = datetime(2026, 10, 1)
    docs = [{"order_no": f"ORD-{i:07d}", "customer_id": rng.randrange(20_000),
             "city": rng.choice(["Karachi", "Lahore", "Islamabad", "Faisalabad"]),
             "status": rng.choice(["pending", "shipped", "delivered", "cancelled"]),
             "created_at": start + timedelta(minutes=rng.randrange(60 * 24 * 27))} for i in range(200_000)]
    scanned, seeked = compare_lookup(docs, "ORD-0123456")
    print(f"lookup by order_no: COLLSCAN examined {scanned:,} | IXSCAN examined {seeked}")
    assert scanned == 200_000 and seeked <= 20

    db = get_db("shop_idx"); db.orders.drop()
    db.orders.insert_many(docs[:2000])
    print(create_indexes(db))
    try:
        db.orders.insert_one({"order_no": "ORD-0000001", "customer_id": 1})
        raise AssertionError("duplicate should fail")
    except DuplicateKeyError:
        print("duplicate order_no rejected")
    week_ago = datetime(2026, 10, 27) - timedelta(days=7)
    n = db.orders.count_documents({"status": "pending", "city": "Karachi", "created_at": {"$gte": week_ago}})
    print("pending Karachi orders in last 7 days (sample):", n)
    assert set(create_indexes(db)) >= {"customer_newest", "status_city_date", "order_no_unique"}
    print("All checks passed")
