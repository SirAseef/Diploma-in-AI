"""Session 01 - Real-life problem: turn spreadsheet rows into well-shaped documents."""
# notebook: run-in-code-dir
from datetime import datetime
from mongo_conn import get_db


def to_doc(row, enrolled):
    doc = {"name": row["name"].strip().title(), "city": row["city"].strip().title(),
           "marks": {"python": int(row["python"]), "sql": int(row["sql"])},
           "skills": [s.strip().lower() for s in row["skills"].split(",") if s.strip()],
           "enrolled": enrolled}
    if row.get("phone", "").strip():
        doc["phone"] = row["phone"].strip()
    return doc


def load_rows(db, rows, enrolled=datetime(2026, 10, 27)):
    db.students.insert_many([to_doc(r, enrolled) for r in rows])
    top = db.students.find_one(sort=[("marks.python", -1)])
    return {"inserted": db.students.count_documents({}),
            "cities": sorted(db.students.distinct("city")),
            "no_phone": db.students.count_documents({"phone": {"$exists": False}}),
            "top_python": top["name"]}


if __name__ == "__main__":
    rows = [
        {"name": "ali raza ", "city": "karachi", "phone": "0300-1111111", "python": "78", "sql": "65", "skills": "Python, Pandas"},
        {"name": "Sana Khan", "city": "Lahore ", "phone": "", "python": "92", "sql": "88", "skills": "python,sql,tableau"},
        {"name": "HAMZA ALI", "city": "Karachi", "phone": "0321-2222222", "python": "55", "sql": "48", "skills": ""},
        {"name": "Zoya Hussain", "city": "hyderabad", "phone": " ", "python": "88", "sql": "70", "skills": "PyTorch"},
    ]
    db = get_db("academy_demo"); db.students.drop()
    summary = load_rows(db, rows)
    print(summary)
    print(db.students.find_one({"name": "Ali Raza"}, {"_id": 0}))
    assert summary == {"inserted": 4, "cities": ["Hyderabad", "Karachi", "Lahore"], "no_phone": 2, "top_python": "Sana Khan"}
    assert db.students.find_one({"name": "Hamza Ali"})["skills"] == []
    print("All checks passed")
