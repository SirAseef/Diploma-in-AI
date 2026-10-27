"""Session 07 - Practice exercise solutions."""
# notebook: run-in-code-dir
import math
from campus_data import seed
from index_sim import build_index, collscan, ixscan
from mongo_conn import get_db

if __name__ == "__main__":
    db = get_db("ex07")
    for c in db.list_collection_names():
        db[c].drop()
    seed(db)
    db.students.create_index([("city", 1), ("marks.sql", -1)])
    names = list(db.students.index_information())
    assert "city_1_marks.sql_-1" in names
    print(names)

    can_use = {"batch": True, "city": False, "batch+city": True, "batch+python": True}
    print("prefix rule for {batch, city, marks.python}:", can_use)

    for n in (1_000, 10_000, 100_000, 1_000_000):
        docs = [{"k": i} for i in range(n)]
        seek = ixscan(build_index(docs, "k"), n // 2)["examined"]
        print(f"N={n:>9,}: scan examines {collscan(docs, 'k', n // 2)['examined']:>9,} | index examines {seek}")
        assert seek <= math.ceil(math.log2(n)) + 1
    print('mongosh: db.students.createIndex({ name: "text", skills: "text" }); db.students.find({ $text: { $search: "python" } })')
    print("All exercise checks passed")
