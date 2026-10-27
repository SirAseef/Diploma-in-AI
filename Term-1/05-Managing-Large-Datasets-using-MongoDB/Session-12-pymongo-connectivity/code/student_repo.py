"""A small repository (data-access) class for students - the same code works on mongomock and a real server."""
from dataclasses import asdict, dataclass, field
from typing import Optional
from pymongo import DESCENDING


@dataclass
class Student:
    name: str
    batch: str
    city: str
    marks: dict = field(default_factory=dict)
    skills: list = field(default_factory=list)
    roll_no: Optional[str] = None


class StudentRepo:
    def __init__(self, db):
        self.coll = db.students
        self.coll.create_index("roll_no", unique=True, sparse=True)   # unique only where roll_no exists
        self.coll.create_index([("batch", 1), ("marks.python", DESCENDING)])

    def add(self, student: Student):
        doc = {k: v for k, v in asdict(student).items() if v is not None}
        return self.coll.insert_one(doc).inserted_id

    def get(self, _id):
        return self.coll.find_one({"_id": _id})

    def add_skill(self, _id, skill):
        return self.coll.update_one({"_id": _id}, {"$addToSet": {"skills": skill}}).modified_count

    def set_mark(self, _id, subject, value):
        if not 0 <= value <= 100:
            raise ValueError("mark must be 0-100")
        return self.coll.update_one({"_id": _id}, {"$set": {f"marks.{subject}": value}}).modified_count

    def top(self, batch, n=3, subject="python"):
        cur = self.coll.find({"batch": batch, f"marks.{subject}": {"$exists": True}}, {"_id": 0, "name": 1, "marks": 1})
        return [(d["name"], d["marks"][subject]) for d in cur.sort(f"marks.{subject}", -1).limit(n)]

    def search_city(self, city, page=1, size=10):
        return [d["name"] for d in self.coll.find({"city": city}, {"_id": 0, "name": 1})
                .sort("name", 1).skip((page - 1) * size).limit(size)]

    def remove(self, _id):
        return self.coll.delete_one({"_id": _id}).deleted_count


if __name__ == "__main__":
    from mongo_conn import get_db
    d = get_db("repo_selftest"); d.students.drop()
    r = StudentRepo(d)
    i = r.add(Student("Test User", "DS-01", "Karachi", {"python": 50}))
    assert r.set_mark(i, "python", 60) == 1 and r.top("DS-01") == [("Test User", 60)]
    print("repo selftest ok")
