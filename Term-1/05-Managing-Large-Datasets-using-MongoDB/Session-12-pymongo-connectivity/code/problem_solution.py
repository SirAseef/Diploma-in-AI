"""Session 12 - Capstone: campus attendance data layer with PyMongo + pandas."""
# notebook: run-in-code-dir
import random
from datetime import date, timedelta
import pandas as pd
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from mongo_conn import get_db


class CampusService:
    def __init__(self, db):
        self.db = db
        db.students.create_index("roll_no", unique=True)
        db.attendance.create_index([("roll_no", 1), ("date", 1)], unique=True)

    def enrol(self, name, batch, city):
        seq = self.db.counters.find_one_and_update({"_id": batch}, {"$inc": {"seq": 1}}, upsert=True,
                                                   return_document=ReturnDocument.AFTER)["seq"]
        roll = f"{batch}-{seq:04d}"
        self.db.students.insert_one({"roll_no": roll, "name": name, "batch": batch, "city": city})
        return roll

    def mark(self, roll_no, day, status):
        self.db.attendance.update_one({"roll_no": roll_no, "date": day}, {"$set": {"status": status}}, upsert=True)

    def monthly_report(self, batch, month):
        rows = list(self.db.attendance.aggregate([
            {"$match": {"roll_no": {"$regex": f"^{batch}-"}, "date": {"$regex": f"^{month}"}}},
            {"$group": {"_id": "$roll_no", "total": {"$sum": 1},
                        "present": {"$sum": {"$cond": [{"$eq": ["$status", "present"]}, 1, 0]}}}},
            {"$lookup": {"from": "students", "localField": "_id", "foreignField": "roll_no", "as": "s"}},
            {"$unwind": "$s"},
            {"$project": {"_id": 0, "roll_no": "$_id", "name": "$s.name", "present": 1, "total": 1}},
        ]))
        df = pd.DataFrame(rows)[["roll_no", "name", "present", "total"]]
        df["pct"] = (100 * df["present"] / df["total"]).round(1)
        return df.sort_values(["pct", "roll_no"], ascending=[False, True]).reset_index(drop=True)

    def at_risk(self, batch, month, threshold=75):
        df = self.monthly_report(batch, month)
        return df.loc[df["pct"] < threshold, "name"].tolist()


if __name__ == "__main__":
    db = get_db("attendance_demo")
    for c in ("students", "attendance", "counters"):
        db[c].drop()
    svc = CampusService(db)
    people = [("Ali Raza", 0.95), ("Sana Khan", 0.9), ("Hamza Ali", 0.6), ("Ayesha Noor", 0.85), ("Usman Tariq", 0.5)]
    rolls = {name: svc.enrol(name, "DS-01", "Karachi") for name, _ in people}
    svc.enrol("Zoya Hussain", "AI-01", "Hyderabad")
    assert rolls["Ali Raza"] == "DS-01-0001" and rolls["Usman Tariq"] == "DS-01-0005"

    rng = random.Random(12)
    days = [date(2026, 10, 1) + timedelta(d) for d in range(31)]
    school_days = [d.isoformat() for d in days if d.weekday() < 5]
    for name, p in people:
        for d in school_days:
            svc.mark(rolls[name], d, "present" if rng.random() < p else "absent")
    svc.mark(rolls["Ali Raza"], school_days[0], "present")          # re-marking must not duplicate
    assert db.attendance.count_documents({"roll_no": rolls["Ali Raza"]}) == len(school_days)
    try:
        db.students.insert_one({"roll_no": "DS-01-0001", "name": "Duplicate"})
        raise AssertionError("duplicate roll number accepted")
    except DuplicateKeyError:
        pass

    report = svc.monthly_report("DS-01", "2026-10")
    risk = svc.at_risk("DS-01", "2026-10")
    print(report)
    print("at risk (<75%):", risk)
    assert len(report) == 5 and (report["total"] == len(school_days)).all()
    assert set(risk) == {"Hamza Ali", "Usman Tariq"}
    print("All checks passed")
