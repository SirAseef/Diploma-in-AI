"""Session 05 - Practice exercise solutions (students collection)."""
# notebook: run-in-code-dir
from mongo_conn import get_db

if __name__ == "__main__":
    db = get_db("exercise_demo")
    db.students.delete_many({})
    db.students.insert_many([
        {"name": "Ali", "batch": "DS-01", "marks": 72},
        {"name": "Sana", "batch": "DS-01", "marks": 88},
        {"name": "Hamza", "batch": "DS-02", "marks": 55},
        {"name": "Zoya", "batch": "DS-02", "marks": 69},
        {"name": "Bilal", "batch": "DS-01", "marks": 64},
    ])
    high = [d["name"] for d in db.students.find({"marks": {"$gte": 70}}).sort("marks", -1)]
    ds01 = list(db.students.find({"batch": "DS-01"}, {"_id": 0, "name": 1, "batch": 1}))
    db.students.update_many({"batch": "DS-02"}, {"$inc": {"marks": 5}})
    avg = list(db.students.aggregate([{"$group": {"_id": "$batch", "avg": {"$avg": "$marks"}}},
                                      {"$sort": {"_id": 1}}]))
    print(high, ds01, avg, sep="\n")
    assert high == ["Sana", "Ali"]
    assert ds01[0] == {"name": "Ali", "batch": "DS-01"} and len(ds01) == 3
    assert db.students.find_one({"name": "Zoya"})["marks"] == 74
    assert avg == [{"_id": "DS-01", "avg": 74.66666666666667}, {"_id": "DS-02", "avg": 67.0}]
    print("All exercise checks passed")
