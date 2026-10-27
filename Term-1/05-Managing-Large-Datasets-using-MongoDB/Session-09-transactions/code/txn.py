"""run_transaction(db, fn, collections): all-or-nothing execution of fn(session).

Real replica set (MONGO_URI set): uses client.start_session() + session.with_transaction(fn).
mongomock (no session support): snapshots the listed collections, calls fn(None), and restores
the snapshot if fn raises - emulating a rollback so the behaviour can be studied without a cluster.
"""
import copy
import os


def run_transaction(db, fn, collections=()):
    if os.environ.get("MONGO_URI"):
        from pymongo import WriteConcern
        with db.client.start_session() as s:
            return s.with_transaction(fn, write_concern=WriteConcern("majority"))
    snapshot = {c: copy.deepcopy(list(db[c].find())) for c in collections}
    try:
        return fn(None)
    except Exception:
        for c, docs in snapshot.items():
            db[c].delete_many({})
            if docs:
                db[c].insert_many(docs)
        raise


if __name__ == "__main__":
    from mongo_conn import get_db
    d = get_db("txn_selftest"); d.a.drop(); d.a.insert_one({"_id": 1, "v": 1})

    def boom(session):
        d.a.update_one({"_id": 1}, {"$set": {"v": 99}}, session=session)
        raise RuntimeError("fail")
    try:
        run_transaction(d, boom, ["a"])
    except RuntimeError:
        pass
    assert d.a.find_one({"_id": 1})["v"] == 1
    print("rollback works")
