"""Python equivalents of common MongoDB Database Tools jobs (teaching helpers)."""
from pathlib import Path
import bson
import pandas as pd
from bson import json_util


def dump_collection(coll, path):
    """Like mongodump for one collection: concatenated BSON documents (readable by bsondump / mongorestore)."""
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(path, "wb") as f:
        for doc in coll.find():
            f.write(bson.encode(doc)); n += 1
    return n


def restore_collection(coll, path):
    docs = bson.decode_all(Path(path).read_bytes())
    if docs:
        coll.insert_many(docs)
    return len(docs)


def export_jsonl(coll, path):
    with open(path, "w", encoding="utf-8") as f:
        for doc in coll.find():
            f.write(json_util.dumps(doc, json_options=json_util.CANONICAL_JSON_OPTIONS) + "\n")


def import_jsonl(coll, path):
    with open(path, encoding="utf-8") as f:
        docs = [json_util.loads(line) for line in f if line.strip()]
    coll.insert_many(docs)
    return len(docs)


def export_csv(coll, path, fields):
    rows = pd.json_normalize(list(coll.find({}, {"_id": 0})))
    rows[fields].to_csv(path, index=False)
    return len(rows)


def import_csv(coll, path, types=None):
    df = pd.read_csv(path, dtype=str).fillna("")
    for col, t in (types or {}).items():
        df[col] = df[col].map(lambda v: t(v) if v != "" else None)
    docs = df.to_dict("records")
    coll.insert_many(docs)
    return len(docs)


def put_file(db, filename, data, chunk_size=255 * 1024):
    """GridFS-style storage: metadata in fs_files, data split into fs_chunks."""
    file_id = db.fs_files.insert_one({"filename": filename, "length": len(data), "chunkSize": chunk_size}).inserted_id
    db.fs_chunks.insert_many([{"files_id": file_id, "n": i, "data": data[o:o + chunk_size]}
                              for i, o in enumerate(range(0, len(data), chunk_size))])
    return file_id


def get_file(db, file_id):
    return b"".join(c["data"] for c in db.fs_chunks.find({"files_id": file_id}).sort("n", 1))


if __name__ == "__main__":
    from mongo_conn import get_db
    d = get_db("tools_selftest"); d.x.drop(); d.x.insert_many([{"a": i} for i in range(3)])
    out = Path("output"); out.mkdir(exist_ok=True)
    assert dump_collection(d.x, out / "x.bson") == 3
    print("selftest ok")
