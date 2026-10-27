"""Session 05 - Real-life problem: clothing store insights from MongoDB."""
# notebook: run-in-code-dir
import pandas as pd
from mongo_conn import get_db


def store_insights(db):
    paid = {"status": "paid"}
    by_cat = list(db.orders.aggregate([
        {"$match": paid},
        {"$unwind": "$items"},
        {"$group": {"_id": "$items.category",
                    "revenue": {"$sum": {"$multiply": ["$items.qty", "$items.price"]}}}},
        {"$sort": {"revenue": -1}},
    ]))
    lines = pd.json_normalize(list(db.orders.find(paid, {"_id": 0})), record_path="items",
                              meta=["customer", "city"])
    lines["total"] = lines["qty"] * lines["price"]
    top_customer = lines.groupby("customer")["total"].sum().idxmax()
    return int(lines["total"].sum()), by_cat, top_customer, lines


if __name__ == "__main__":
    db = get_db("store_demo")
    db.orders.delete_many({})
    db.orders.insert_many([
        {"customer": "Ali", "city": "Karachi", "status": "paid",
         "items": [{"category": "men", "qty": 2, "price": 3000}, {"category": "shoes", "qty": 1, "price": 5500}]},
        {"customer": "Sana", "city": "Karachi", "status": "paid",
         "items": [{"category": "women", "qty": 3, "price": 4000}]},
        {"customer": "Omar", "city": "Hyderabad", "status": "cancelled",
         "items": [{"category": "men", "qty": 5, "price": 3000}]},
        {"customer": "Ali", "city": "Karachi", "status": "paid",
         "items": [{"category": "women", "qty": 1, "price": 4500}]},
    ])
    total, by_cat, top, lines = store_insights(db)
    print("Revenue:", total, "| top customer:", top)
    print(by_cat)
    print(lines)
    assert total == 6000 + 5500 + 12000 + 4500
    assert by_cat[0] == {"_id": "women", "revenue": 16500}
    assert top == "Ali"   # 6000 + 5500 + 4500 = 16000 vs Sana 12000
    print("All checks passed")
