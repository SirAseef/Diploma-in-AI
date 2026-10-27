"""Session 06 - Practice exercise solutions."""
# notebook: run-in-code-dir
from campus_data import seed
from mongo_conn import get_db

if __name__ == "__main__":
    db = get_db("ex06")
    for c in db.list_collection_names():
        db[c].drop()
    seed(db)
    ranks = [d["name"] for d in db.students.find().sort("marks.sql", -1).skip(3).limit(3)]
    print("4th-6th by SQL:", ranks)
    assert ranks == ["Hina Shah", "Bilal Ahmed", "Zoya Hussain"]
    lines = [f"{d['name']}: {len(d['skills'])} skills" for d in db.students.find({"batch": "AI-01"}).sort("student_id", 1)]
    print(lines)
    assert lines[0] == "Bilal Ahmed: 2 skills"
    removed = db.students.find_one_and_delete({}, sort=[("marks.python", 1)])
    assert removed["name"] == "Usman Tariq" and db.students.count_documents({}) == 9
    print("removed:", removed["name"])
    print('mongosh: db.students.find({ city: "Karachi" }).forEach(s => print(s.name.toUpperCase()))')
    print("All exercise checks passed")
