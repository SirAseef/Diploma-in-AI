"""Session 12 - PyMongo connectivity: worked examples."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Setup

# %%
import pandas as pd
from campus_data import seed
from mongo_conn import backend, get_db
print("Backend:", backend())
db = get_db("campus_py")
for c in db.list_collection_names():
    db[c].drop()
print(seed(db))

# %% [markdown]
# ## Example 1 - result objects

# %%
r = db.students.insert_one({"name": "Iqra Shah", "batch": "DS-02", "city": "Karachi", "marks": {"python": 70}})
print("inserted:", r.inserted_id)
u = db.students.update_many({"batch": "DS-02"}, {"$set": {"room": 2}})
print("matched", u.matched_count, "| modified", u.modified_count)
d = db.students.delete_one({"name": "Nobody"})
print("deleted", d.deleted_count)

# %% [markdown]
# ## Example 2 - ObjectId round trip

# %%
from bson import ObjectId
from bson.errors import InvalidId

def get_by_id(text):
    try:
        return db.students.find_one({"_id": ObjectId(text)}, {"_id": 0, "name": 1})
    except InvalidId:
        return None

text_id = str(r.inserted_id)                   # as it would arrive in a URL
print(get_by_id(text_id), get_by_id("not-an-id"))

# %% [markdown]
# ## Example 3 - a repository class

# %%
from student_repo import Student, StudentRepo
repo = StudentRepo(db)
sid = repo.add(Student(name="Danish Ali", batch="AI-01", city="Karachi", marks={"python": 74}, roll_no="AI-01-0001"))
repo.add_skill(sid, "mongodb")
print(repo.get(sid)["skills"], repo.top(batch="AI-01", n=3))

# %% [markdown]
# ## Example 4 - handling errors

# %%
from pymongo.errors import DuplicateKeyError
try:
    repo.add(Student(name="Copy Cat", batch="AI-01", city="Lahore", roll_no="AI-01-0001"))
except DuplicateKeyError:
    print("roll number already used")
try:
    repo.set_mark(sid, "python", 140)
except ValueError as e:
    print("rejected:", e)

# %% [markdown]
# ## Example 5 - batch processing with a generator

# %%
def batches(cursor, size=500):
    batch = []
    for doc in cursor:
        batch.append(doc)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch

db.events.drop()
db.events.insert_many([{"n": i} for i in range(1234)])
print([len(b) for b in batches(db.events.find(), 500)])

# %% [markdown]
# ## Example 6 - aggregation into pandas

# %%
df = pd.DataFrame(db.students.aggregate([
    {"$group": {"_id": "$batch", "students": {"$sum": 1}, "avg_python": {"$avg": "$marks.python"}}},
    {"$sort": {"_id": 1}}])).rename(columns={"_id": "batch"})
df["avg_python"] = df["avg_python"].round(1)
print(df)
