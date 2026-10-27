"""Session 04 - Aggregation pipeline: worked examples on the campus sample data."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Setup

# %%
from campus_data import seed
from mongo_conn import get_db
db = get_db("campus_agg")
print(seed(db))

def show(rows):
    for r in rows:
        print(r)

# %% [markdown]
# ## Example 1 - count and average per batch

# %%
rows = list(db.students.aggregate([
    {"$group": {"_id": "$batch", "students": {"$sum": 1}, "avg_python": {"$avg": "$marks.python"}}},
    {"$sort": {"_id": 1}},
]))
show({**r, "avg_python": round(r["avg_python"], 1)} for r in rows)
assert [r["students"] for r in rows] == [4, 3, 3]

# %% [markdown]
# ## Example 2 - computed fields and grades

# %%
show(db.students.aggregate([
    {"$addFields": {"total": {"$add": ["$marks.python", "$marks.sql", "$marks.stats"]}}},
    {"$addFields": {"grade": {"$switch": {"branches": [
        {"case": {"$gte": ["$total", 240]}, "then": "A"},
        {"case": {"$gte": ["$total", 180]}, "then": "B"}], "default": "C"}}}},
    {"$project": {"_id": 0, "name": 1, "total": 1, "grade": 1}},
    {"$sort": {"total": -1}},
]))

# %% [markdown]
# ## Example 3 - $unwind: most common skills

# %%
top_skills = list(db.students.aggregate([{"$unwind": "$skills"}, {"$group": {"_id": "$skills", "n": {"$sum": 1}}},
                                         {"$sort": {"n": -1, "_id": 1}}, {"$limit": 3}]))
show(top_skills)
assert top_skills[0] == {"_id": "python", "n": 7}

# %% [markdown]
# ## Example 4 - $lookup: fees collected per city

# %%
show(db.payments.aggregate([
    {"$lookup": {"from": "students", "localField": "student_id", "foreignField": "student_id", "as": "s"}},
    {"$unwind": "$s"},
    {"$group": {"_id": "$s.city", "collected": {"$sum": "$amount"}}},
    {"$sort": {"collected": -1}},
]))

# %% [markdown]
# ## Example 5 - $bucket and $facet

# %%
facet = list(db.students.aggregate([{"$facet": {
    "python_bands": [{"$bucket": {"groupBy": "$marks.python", "boundaries": [0, 50, 70, 90, 101],
                                  "output": {"n": {"$sum": 1}}}}],
    "karachi": [{"$match": {"city": "Karachi"}}, {"$count": "n"}],
}}]))[0]
print(facet)

# %% [markdown]
# ## Example 6 - top student per batch, saved with $out

# %%
db.students.aggregate([
    {"$sort": {"marks.python": -1}},
    {"$group": {"_id": "$batch", "top": {"$first": "$name"}, "score": {"$first": "$marks.python"}}},
    {"$out": "top_students"},
])
show(db.top_students.find().sort("_id", 1))
