"""Session 04 - Real-life problem: monthly and batch fee reports with aggregation."""
# notebook: run-in-code-dir
from campus_data import seed
from mongo_conn import get_db


def monthly_report(db):
    return list(db.payments.aggregate([
        {"$group": {"_id": {"month": "$month", "method": "$method"}, "amount": {"$sum": "$amount"}, "n": {"$sum": 1}}},
        {"$group": {"_id": "$_id.month", "total": {"$sum": "$amount"}, "payments": {"$sum": "$n"},
                    "by_method": {"$push": {"method": "$_id.method", "amount": "$amount"}}}},
        {"$sort": {"_id": 1}},
    ]))


def batch_report(db):
    db.students.aggregate([
        {"$lookup": {"from": "payments", "localField": "student_id", "foreignField": "student_id", "as": "pays"}},
        {"$addFields": {"paid": {"$sum": "$pays.amount"}, "n_pays": {"$size": "$pays"}}},
        {"$group": {"_id": "$batch", "collected": {"$sum": "$paid"},
                    "never_paid": {"$push": {"$cond": [{"$eq": ["$n_pays", 0]}, "$name", None]}}}},
        {"$sort": {"_id": 1}},
        {"$out": "fee_report"},
    ])
    rows = list(db.fee_report.find().sort("_id", 1))
    for r in rows:
        r["never_paid"] = sorted(n for n in r["never_paid"] if n)
    return rows


if __name__ == "__main__":
    db = get_db("fees_demo"); seed(db)
    months = monthly_report(db)
    for m in months:
        print(m["_id"], m["total"], m["payments"], sorted((x["method"], x["amount"]) for x in m["by_method"]))
    batches = batch_report(db)
    for b in batches:
        print(b["_id"], b["collected"], b["never_paid"])
    assert [m["_id"] for m in months] == ["2026-01", "2026-02", "2026-03", "2026-04"]
    assert sum(m["total"] for m in months) == 180_000
    assert next(m for m in months if m["_id"] == "2026-02")["payments"] == 5
    by_batch = {b["_id"]: b for b in batches}
    assert by_batch["DS-01"]["never_paid"] == ["Usman Tariq"]
    assert by_batch["AI-01"]["never_paid"] == ["Mariam Javed"]
    assert by_batch["DS-02"]["collected"] == 48_000
    print("All checks passed")
