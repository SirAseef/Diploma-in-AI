"""Session 03 - Practice exercise solutions."""
# notebook: run-in-code-dir
from campus_data import seed
from mongo_conn import get_db

if __name__ == "__main__":
    db = get_db("ex03"); seed(db)
    q1 = sorted(d["name"] for d in db.students.find({"marks.python": {"$gte": 60, "$lte": 80}, "batch": {"$ne": "AI-01"}}))
    assert q1 == ["Ali Raza"]
    q2 = sorted(d["name"] for d in db.students.find({"phone": {"$exists": True}, "skills.2": {"$exists": True}}))
    assert q2 == ["Faraz Iqbal", "Sana Khan"]
    db.students.update_many({}, {"$rename": {"city": "home_city"}})
    for _ in range(2):
        db.students.update_one({"name": "Faraz Iqbal"}, {"$addToSet": {"skills": "tableau"}})
    faraz = db.students.find_one({"name": "Faraz Iqbal"})
    assert "city" not in faraz and faraz["home_city"] == "Karachi" and faraz["skills"].count("tableau") == 1
    db.students.update_many({"skills.3": {"$exists": True}}, {"$pop": {"skills": 1}})
    assert db.students.find_one({"name": "Faraz Iqbal"})["skills"] == ["python", "sql", "mongodb", "spark"]
    print(q1, q2, "All exercise checks passed")
