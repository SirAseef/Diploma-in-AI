"""run(db, name, *args, **kw): call a MongoDB database command.

Real server (MONGO_URI set): delegates to db.command(...).
mongomock: emulates the most common read-only commands in plain Python so their output can be studied.
Sizes are computed from BSON encoding (dataSize = uncompressed BSON bytes, like the real server).
"""
import os
import bson


def _size(docs):
    return sum(len(bson.encode(d)) for d in docs)


def _coll_stats(db, name):
    docs = list(db[name].find())
    size = _size(docs)
    return {"ns": f"{db.name}.{name}", "count": len(docs), "size": size,
            "avgObjSize": size // len(docs) if docs else 0, "nindexes": len(db[name].index_information()), "ok": 1.0}


def run(db, name, *args, **kw):
    if os.environ.get("MONGO_URI"):
        if name == "collStats":   # modern servers: $collStats aggregation stage
            out = list(db[args[0]].aggregate([{"$collStats": {"storageStats": {}}}]))[0]["storageStats"]
            return {"count": out["count"], "size": out["size"], "avgObjSize": out.get("avgObjSize", 0), "ok": 1.0}
        if name in ("count", "distinct"):
            return db.command(name, args[0], **kw)
        return db.command(name, *args, **kw)
    if name == "ping":
        return {"ok": 1.0}
    if name == "buildInfo":
        return {"version": "mongomock (emulated)", "ok": 1.0}
    if name == "listCollections":
        return {"cursor": {"firstBatch": [{"name": n, "type": "collection"} for n in sorted(db.list_collection_names())]}, "ok": 1.0}
    if name == "collStats":
        return _coll_stats(db, args[0])
    if name == "dbStats":
        stats = [_coll_stats(db, n) for n in db.list_collection_names()]
        objects = sum(s["count"] for s in stats); size = sum(s["size"] for s in stats)
        return {"db": db.name, "collections": len(stats), "objects": objects, "dataSize": size,
                "avgObjSize": size // objects if objects else 0, "indexes": sum(s["nindexes"] for s in stats), "ok": 1.0}
    if name == "count":
        return {"n": db[args[0]].count_documents(kw.get("query", {})), "ok": 1.0}
    if name == "distinct":
        return {"values": sorted(db[args[0]].distinct(kw["key"], kw.get("query", {}))), "ok": 1.0}
    raise NotImplementedError(f"{name} is not emulated; run it on a real MongoDB server")


if __name__ == "__main__":
    from mongo_conn import get_db
    d = get_db("cmd_selftest"); d.x.drop(); d.x.insert_many([{"a": 1}, {"a": 2}])
    assert run(d, "collStats", "x")["count"] == 2 and run(d, "ping")["ok"] == 1.0
    print(run(d, "dbStats"))
