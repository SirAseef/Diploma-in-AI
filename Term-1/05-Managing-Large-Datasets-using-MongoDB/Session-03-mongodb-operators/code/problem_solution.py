"""Session 03 - Real-life problem: quiz results with array operators."""
# notebook: run-in-code-dir
from mongo_conn import get_db


def strong_in_sql(db):
    return sorted(d["name"] for d in db.quizzes.find({"tests": {"$elemMatch": {"topic": "sql", "score": {"$gte": 8}}}}))


def few_tests(db):
    return sorted(d["name"] for d in db.quizzes.find({"$or": [{"tests": {"$exists": False}}, {"tests": {"$size": 0}},
                                                              {"tests": {"$size": 1}}]}))


def add_test(db, name, topic, score):
    db.quizzes.update_one({"name": name}, {"$push": {"tests": {"$each": [{"topic": topic, "score": score}], "$slice": -5}}})


def grace_stats(db):
    for d in db.quizzes.find({"tests.topic": "stats"}):
        db.quizzes.update_one({"_id": d["_id"], "tests.topic": "stats"}, {"$inc": {"tests.$.score": 1}})
        db.quizzes.update_one({"_id": d["_id"], "tests": {"$elemMatch": {"topic": "stats", "score": {"$gt": 10}}}},
                              {"$set": {"tests.$.score": 10}})


def mark_attendance(db, name, date, status):
    db.attendance.update_one({"name": name, "date": date}, {"$set": {"status": status}}, upsert=True)


if __name__ == "__main__":
    db = get_db("quiz_demo"); db.quizzes.drop(); db.attendance.drop()
    db.quizzes.insert_many([
        {"name": "Ali", "batch": "DS-01", "tests": [{"topic": "sql", "score": 6}, {"topic": "python", "score": 9}]},
        {"name": "Sana", "batch": "DS-01", "tests": [{"topic": "sql", "score": 9}, {"topic": "stats", "score": 10}]},
        {"name": "Hamza", "batch": "DS-02", "tests": [{"topic": "stats", "score": 5}]},
        {"name": "Zoya", "batch": "AI-01"},
        {"name": "Omar", "batch": "AI-01", "tests": [{"topic": "sql", "score": 8}, {"topic": "stats", "score": 7}]},
    ])
    assert strong_in_sql(db) == ["Omar", "Sana"]
    assert few_tests(db) == ["Hamza", "Zoya"]
    for i, (t, s) in enumerate([("python", 7), ("sql", 8), ("stats", 6), ("ml", 9)]):
        add_test(db, "Ali", t, s)
    ali = db.quizzes.find_one({"name": "Ali"})["tests"]
    assert len(ali) == 5 and ali[0] == {"topic": "python", "score": 9} and ali[-1]["topic"] == "ml"
    grace_stats(db)
    stats = {d["name"]: next(t["score"] for t in d["tests"] if t["topic"] == "stats") for d in db.quizzes.find({"tests.topic": "stats"})}
    print("stats after grace:", stats)
    assert stats["Sana"] == 10 and stats["Hamza"] == 6 and stats["Omar"] == 8 and stats["Ali"] == 7
    for _ in range(3):
        mark_attendance(db, "Ali", "2026-10-27", "present")
    mark_attendance(db, "Ali", "2026-10-27", "late")
    assert db.attendance.count_documents({}) == 1 and db.attendance.find_one()["status"] == "late"
    print("All checks passed")
