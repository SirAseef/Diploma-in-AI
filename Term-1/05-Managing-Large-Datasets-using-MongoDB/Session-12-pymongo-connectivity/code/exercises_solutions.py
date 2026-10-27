"""Session 12 - Practice exercise solutions."""
# notebook: run-in-code-dir
import json
from datetime import datetime
from bson import ObjectId
from campus_data import seed
from mongo_conn import get_db
from student_repo import StudentRepo


def to_json_safe(doc):
    return {k: str(v) if isinstance(v, ObjectId) else v.isoformat() if isinstance(v, datetime) else v
            for k, v in doc.items()}


def batches(cursor, size=500):
    batch = []
    for doc in cursor:
        batch.append(doc)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


if __name__ == "__main__":
    db = get_db("ex12")
    for c in db.list_collection_names():
        db[c].drop()
    r = db.s.insert_many([{"n": 1}, {"n": 2}, {"n": 3}])
    assert len(r.inserted_ids) == 3
    u = db.s.update_one({"n": 2}, {"$set": {"flag": True}})
    assert (u.matched_count, u.modified_count) == (1, 1)
    u2 = db.s.update_one({"n": 2}, {"$set": {"flag": True}})
    assert (u2.matched_count, u2.modified_count) == (1, 0)

    seed(db)
    doc = db.students.find_one({"student_id": 1})
    print(json.dumps(to_json_safe(doc))[:90], "...")

    repo = StudentRepo(db)
    assert repo.search_city("Karachi", page=1, size=3) == ["Ali Raza", "Bilal Ahmed", "Faraz Iqbal"]
    assert repo.search_city("Karachi", page=2, size=3) == ["Hamza Ali", "Usman Tariq"]

    db.big.insert_many([{"i": i} for i in range(1234)])
    assert [len(b) for b in batches(db.big.find(), 500)] == [500, 500, 234]
    print("All exercise checks passed")
