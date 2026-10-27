"""Session 02 - Practice exercise solutions."""
# notebook: run-in-code-dir
import re
from pymongo.errors import BulkWriteError
from mongo_conn import get_client
from schema_check import STUDENT_SCHEMA, check

if __name__ == "__main__":
    client = get_client()
    lib = client["library"]; lib.books.insert_one({"title": "Python for Everyone"})
    assert "books" in lib.list_collection_names()
    client.drop_database("library")
    assert "library" not in client.list_database_names()

    db = client["ex02"]
    docs = [{"_id": i} for i in (1, 2, 2, 3, 4)]
    inserted = {}
    for ordered in (True, False):
        db.c.drop()
        try:
            db.c.insert_many([dict(d) for d in docs], ordered=ordered)
        except BulkWriteError as e:
            inserted[ordered] = e.details["nInserted"]
    print("inserted (ordered, unordered):", inserted)
    assert inserted == {True: 2, False: 4}

    db.students.drop()
    db.students.insert_many([{"name": "Ali", "course_ids": ["PY101"]}, {"name": "Sana", "course_ids": ["PY101", "DB201"]},
                             {"name": "Omar", "course_ids": ["DB201", "ST110"]}])
    assert sorted(s["name"] for s in db.students.find({"course_ids": "DB201"})) == ["Omar", "Sana"]

    def check_phone(doc):
        problems = check(doc, STUDENT_SCHEMA)
        if "phone" in doc and not re.fullmatch(r"03\d{2}-\d{7}", doc["phone"]) and "phone has wrong format" not in problems:
            problems.append("phone has wrong format")
        return problems
    assert check_phone({"name": "Sana", "batch": "DS-01", "marks": {}, "phone": "0300-1234567"}) == []
    assert "phone has wrong format" in check_phone({"name": "Sana", "batch": "DS-01", "marks": {}, "phone": "300-12"})
    print("All exercise checks passed")
