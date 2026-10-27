"""Session 05 - Practice exercise solutions."""
# notebook: run-in-code-dir
from campus_data import seed
from commands import run
from mongo_conn import get_db

if __name__ == "__main__":
    db = get_db("ex05")
    for c in db.list_collection_names():
        db[c].drop()
    seed(db)
    n = run(db, "count", "students", query={"batch": "AI-01"})["n"]
    assert n == db.students.count_documents({"batch": "AI-01"}) == 4
    cities = run(db, "distinct", "students", key="city", query={"marks.python": {"$gte": 80}})["values"]
    assert cities == ["Hyderabad", "Islamabad", "Karachi", "Lahore"]
    total = run(db, "dbStats")["dataSize"]
    shares = {c: round(100 * run(db, "collStats", c)["size"] / total, 1) for c in db.list_collection_names()}
    print("share of dataSize %:", shares)
    assert abs(sum(shares.values()) - 100) < 0.5 and max(shares, key=shares.get) == "students"
    print('db.createUser({ user: "fee_clerk", pwd: passwordPrompt(), roles: [ { role: "readWrite", db: "campus" } ] })')
    print("All exercise checks passed")
