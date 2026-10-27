"""Session 03 - MongoDB operators: worked examples on the campus sample data."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Setup

# %%
from campus_data import seed
from mongo_conn import get_db
db = get_db("campus_ops")
print(seed(db))

def names(cursor):
    return [d["name"] for d in cursor]

# %% [markdown]
# ## Example 1 - comparison and logical

# %%
print(names(db.students.find({"marks.python": {"$gte": 80}, "city": {"$in": ["Karachi", "Lahore"]}})))
print(names(db.students.find({"$or": [{"city": "Quetta"}, {"marks.sql": {"$lt": 50}}]})))
print(names(db.students.find({"$nor": [{"city": "Karachi"}, {"city": "Lahore"}]})))
print(names(db.students.find({"marks.python": {"$not": {"$gte": 60}}})))

# %% [markdown]
# ## Example 2 - element and evaluation

# %%
print("no phone:", names(db.students.find({"phone": {"$exists": False}})))
print("name starts with A:", names(db.students.find({"name": {"$regex": "^a", "$options": "i"}})))
print("sql > python:", names(db.students.find({"$expr": {"$gt": ["$marks.sql", "$marks.python"]}})))

# %% [markdown]
# ## Example 3 - array queries

# %%
print("knows python:", len(names(db.students.find({"skills": "python"}))))
print("python AND sql:", names(db.students.find({"skills": {"$all": ["python", "sql"]}})))
print("no skills:", names(db.students.find({"skills": {"$size": 0}})))
db.quizzes.drop()
db.quizzes.insert_many([
    {"name": "Ali", "tests": [{"topic": "sql", "score": 6}, {"topic": "python", "score": 9}]},
    {"name": "Sana", "tests": [{"topic": "sql", "score": 9}, {"topic": "stats", "score": 7}]},
])
print("dot-notation (different elements):", names(db.quizzes.find({"tests.topic": "sql", "tests.score": {"$gte": 8}})))
print("$elemMatch (same element):", names(db.quizzes.find({"tests": {"$elemMatch": {"topic": "sql", "score": {"$gte": 8}}}})))

# %% [markdown]
# ## Example 4 - projections

# %%
for d in db.students.find({"batch": "DS-01"}, {"_id": 0, "name": 1, "skills": {"$slice": 1}}):
    print(d)

# %% [markdown]
# ## Example 5 - field updates and upsert

# %%
db.students.update_one({"student_id": 1}, {"$inc": {"marks.sql": 5}, "$min": {"marks.stats": 60},
                                           "$rename": {"phone": "mobile"}, "$currentDate": {"updated": True}})
print(db.students.find_one({"student_id": 1}, {"_id": 0, "marks": 1, "mobile": 1}))
for _ in range(2):
    db.attendance.update_one({"student_id": 1, "date": "2026-10-27"}, {"$set": {"status": "present"}}, upsert=True)
print("attendance docs:", db.attendance.count_documents({}))

# %% [markdown]
# ## Example 6 - array updates

# %%
db.students.update_one({"student_id": 1}, {"$addToSet": {"skills": "sql"}})
db.students.update_one({"student_id": 1}, {"$addToSet": {"skills": "sql"}})       # no duplicate
db.students.update_many({}, {"$pull": {"skills": "excel"}})
db.quizzes.update_one({"name": "Ali"}, {"$push": {"tests": {"$each": [{"topic": "stats", "score": 8}],
                                                             "$sort": {"score": -1}, "$slice": 2}}})
db.quizzes.update_one({"name": "Ali", "tests.topic": "stats"}, {"$set": {"tests.$.score": 10}})
print(db.students.find_one({"student_id": 1})["skills"], db.students.count_documents({"skills": "excel"}))
print(db.quizzes.find_one({"name": "Ali"}, {"_id": 0}))
