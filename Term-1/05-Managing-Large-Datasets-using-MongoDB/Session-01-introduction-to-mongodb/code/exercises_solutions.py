"""Session 01 - Practice exercise solutions."""
# notebook: run-in-code-dir
from campus_data import seed
from mongo_conn import get_db

if __name__ == "__main__":
    db = get_db("ex01")
    db.courses.drop()
    db.courses.insert_many([
        {"code": "PY101", "title": "Python Basics", "hours": 36, "tags": ["python"]},
        {"code": "DB201", "title": "MongoDB Essentials", "hours": 24, "tags": ["nosql", "mongodb"]},
        {"code": "ST110", "title": "Statistics", "hours": 30, "tags": ["math", "stats"]},
    ])
    courses = list(db.courses.find({}, {"_id": 0}))
    assert len(courses) == 3 and "_id" not in courses[0]

    counts = seed(db)
    karachi = db.students.count_documents({"city": "Karachi"})
    batches = sorted(db.students.distinct("batch"))
    oid = db.notes.insert_one({"text": "hello"}).inserted_id
    print(counts, "| Karachi students:", karachi, "| batches:", batches, "| note created:", oid.generation_time)
    assert karachi == 5 and batches == ["AI-01", "DS-01", "DS-02"]
    print("All exercise checks passed")
