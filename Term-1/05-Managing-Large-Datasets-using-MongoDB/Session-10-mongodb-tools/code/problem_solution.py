"""Session 10 - Real-life problem: back up, restore, verify, and export a report."""
# notebook: run-in-code-dir
import hashlib
import json
from pathlib import Path
import bson
import pandas as pd
from campus_data import seed
from mongo_conn import get_client
from tools_py import dump_collection, restore_collection


def backup(db, folder):
    folder.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name in sorted(db.list_collection_names()):
        manifest[name] = dump_collection(db[name], folder / f"{name}.bson")
    (folder / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def restore(db, folder):
    manifest = json.loads((folder / "manifest.json").read_text())
    for name in manifest:
        db[name].drop()
        restore_collection(db[name], folder / f"{name}.bson")
    return manifest


def checksum(coll):
    return hashlib.sha256(b"".join(sorted(bson.encode(d) for d in coll.find()))).hexdigest()


def verify(src, dst):
    return all(src[n].count_documents({}) == dst[n].count_documents({}) and checksum(src[n]) == checksum(dst[n])
               for n in src.list_collection_names())


if __name__ == "__main__":
    client = get_client()
    src = client["campus_prod"]
    for c in src.list_collection_names():
        src[c].drop()
    seed(src)
    folder = Path("output/backup/2026-10-27")
    manifest = backup(src, folder)
    print("manifest:", manifest)
    dst = client["campus_after_upgrade"]
    restore(dst, folder)
    ok = verify(src, dst)
    print("verified:", ok)
    assert manifest == {"batches": 3, "payments": 12, "students": 10} and ok
    dst.students.delete_one({"student_id": 3})
    assert not verify(src, dst)                         # verification catches a missing document
    report = pd.json_normalize(list(src.students.find({}, {"_id": 0, "name": 1, "batch": 1, "marks": 1})))
    report["average"] = report[["marks.python", "marks.sql", "marks.stats"]].mean(axis=1).round(1)
    report.sort_values("average", ascending=False).to_csv("output/principal_report.csv", index=False)
    print(report.sort_values("average", ascending=False).head(3))
    print("All checks passed")
