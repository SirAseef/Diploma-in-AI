"""Session 04 - Practice exercise solutions."""
# notebook: run-in-code-dir
from campus_data import seed
from mongo_conn import get_db

TOTAL = {"$add": ["$marks.python", "$marks.sql", "$marks.stats"]}

if __name__ == "__main__":
    db = get_db("ex04"); seed(db)
    by_city = list(db.students.aggregate([{"$group": {"_id": "$city", "avg_sql": {"$avg": "$marks.sql"}}},
                                          {"$sort": {"avg_sql": -1}}]))
    assert by_city[0]["_id"] == "Islamabad"          # Ayesha's 90

    skills = {r["_id"]: sorted(r["skills"]) for r in db.students.aggregate(
        [{"$unwind": "$skills"}, {"$group": {"_id": "$batch", "skills": {"$addToSet": "$skills"}}}])}
    assert skills["DS-01"] == ["pandas", "python", "sql", "tableau"]

    per_month = list(db.students.aggregate([
        {"$group": {"_id": {"$dateToString": {"format": "%Y-%m", "date": "$enrolled"}}, "n": {"$sum": 1}}},
        {"$sort": {"_id": 1}}]))
    assert per_month == [{"_id": "2026-01", "n": 3}, {"_id": "2026-02", "n": 4}, {"_id": "2026-03", "n": 3}]

    avg = list(db.students.aggregate([{"$group": {"_id": None, "avg": {"$avg": TOTAL}}}]))[0]["avg"]
    above = sorted(d["name"] for d in db.students.aggregate([{"$addFields": {"total": TOTAL}},
                                                             {"$match": {"total": {"$gt": avg}}}]))
    print("average total", round(avg, 1), "| above:", above)
    assert above == ["Ayesha Noor", "Faraz Iqbal", "Hina Shah", "Sana Khan", "Zoya Hussain"]
    print("All exercise checks passed")
