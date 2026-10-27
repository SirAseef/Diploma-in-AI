"""Session 10 - Practice exercise solutions."""
# notebook: run-in-code-dir
import math
from datetime import datetime
from pathlib import Path
import pandas as pd
from campus_data import seed
from mongo_conn import get_client
from tools_py import export_csv, export_jsonl, import_jsonl

if __name__ == "__main__":
    print("mongodump --db=campus --collection=payments --out=dump/")
    print('mongorestore --nsFrom="campus.payments" --nsTo="campus_test.payments" dump/')
    out = Path("output"); out.mkdir(exist_ok=True)
    client = get_client()
    db = client["ex10"]
    for c in db.list_collection_names():
        db[c].drop()
    seed(db)
    export_jsonl(db.students, out / "students.jsonl")
    db2 = client["ex10_copy"]; db2.students.drop()
    assert import_jsonl(db2.students, out / "students.jsonl") == 10
    assert isinstance(db2.students.find_one()["enrolled"], datetime)

    export_csv(db.students, out / "stats.csv", fields=["name", "batch", "marks.stats"])
    dtype = pd.read_csv(out / "stats.csv")["marks.stats"].dtype
    print("marks.stats dtype after CSV round trip:", dtype)
    assert str(dtype) == "int64"

    assert math.ceil(1_000_000 / (255 * 1024)) == 4
    print("All exercise checks passed")
