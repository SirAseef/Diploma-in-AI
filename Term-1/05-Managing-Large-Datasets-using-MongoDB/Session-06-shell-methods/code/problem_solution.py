"""Session 06 - Real-life problem: portal pagination, roll numbers and streamed reports."""
# notebook: run-in-code-dir
import random
from pymongo import ReturnDocument
from mongo_conn import get_db


def page_by_skip(db, page, size=10):
    cur = db.people.find({}, {"_id": 0, "name": 1}).sort("name", 1).skip((page - 1) * size).limit(size)
    return [d["name"] for d in cur]


def page_by_range(db, after_name=None, size=10):
    flt = {"name": {"$gt": after_name}} if after_name else {}
    return [d["name"] for d in db.people.find(flt, {"_id": 0, "name": 1}).sort("name", 1).limit(size)]


def next_roll_no(db, batch):
    c = db.counters.find_one_and_update({"_id": batch}, {"$inc": {"seq": 1}}, upsert=True,
                                        return_document=ReturnDocument.AFTER)
    return f"{batch}-{c['seq']:04d}"


def cursor_report(db):
    summary = {}
    for doc in db.people.find({}, {"city": 1}):
        summary[doc["city"]] = summary.get(doc["city"], 0) + 1
    return dict(sorted(summary.items()))


if __name__ == "__main__":
    rng = random.Random(6)
    first = ["Ali", "Sana", "Hamza", "Ayesha", "Bilal", "Zoya", "Usman", "Hina", "Faraz", "Mariam", "Omar", "Iqra"]
    last = ["Khan", "Ahmed", "Raza", "Shah", "Iqbal", "Malik", "Siddiqui", "Qureshi"]
    names = sorted({f"{f} {l}" for f in first for l in last})
    chosen = rng.sample(names, 47)
    db = get_db("portal_demo"); db.people.drop(); db.counters.drop()
    db.people.insert_many([{"name": n, "city": rng.choice(["Karachi", "Lahore", "Hyderabad"])} for n in chosen])
    pages_skip = [page_by_skip(db, p) for p in range(1, 6)]
    pages_range, last_seen = [], None
    while True:
        page = page_by_range(db, last_seen)
        if not page:
            break
        pages_range.append(page); last_seen = page[-1]
    print("page 1:", pages_skip[0][:3], "... | pages:", len(pages_range), "| last page size:", len(pages_range[-1]))
    assert pages_skip == pages_range and len(pages_range) == 5 and len(pages_range[-1]) == 7
    rolls = [next_roll_no(db, "DS-01") for _ in range(3)] + [next_roll_no(db, "AI-01")]
    print(rolls)
    assert rolls == ["DS-01-0001", "DS-01-0002", "DS-01-0003", "AI-01-0001"]
    report = cursor_report(db)
    print(report)
    assert sum(report.values()) == 47
    print("All checks passed")
