"""Session 05 - Real-life problem: nightly collection health report."""
# notebook: run-in-code-dir
from campus_data import seed
from commands import run
from mongo_conn import get_db


def health_report(db, big_doc_bytes=400):
    if run(db, "ping").get("ok") != 1:
        raise RuntimeError("server not reachable")
    report = []
    for name in sorted(db.list_collection_names()):
        cs = run(db, "collStats", name)
        flags = []
        if cs["count"] == 0:
            flags.append("empty")
        elif cs["avgObjSize"] > big_doc_bytes:
            flags.append("large documents")
        report.append({"collection": name, "count": cs["count"], "size": cs["size"],
                       "avgObjSize": cs["avgObjSize"], "flags": flags})
    return sorted(report, key=lambda r: r["size"], reverse=True)


if __name__ == "__main__":
    db = get_db("health_demo")
    for c in db.list_collection_names():
        db[c].drop()
    seed(db)
    db.create_collection("audit_log")                                          # empty collection
    db.sensors.insert_one({"device": "AC-12", "readings": [{"t": i, "temp": 24 + i % 5} for i in range(60)]})
    report = health_report(db)
    for r in report:
        print(r)
    flags = {r["collection"]: r["flags"] for r in report}
    assert flags["audit_log"] == ["empty"]
    assert flags["sensors"] == ["large documents"]
    assert flags["students"] == [] and report[0]["collection"] in ("students", "sensors")
    print("All checks passed")
