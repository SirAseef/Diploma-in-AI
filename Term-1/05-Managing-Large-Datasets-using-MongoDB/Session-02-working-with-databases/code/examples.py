"""Session 02 - Working with MongoDB databases: worked examples."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - databases and collections

# %%
from mongo_conn import get_client
client = get_client()
db = client["campus_admin"]
for c in db.list_collection_names():
    db[c].drop()
db.notices.insert_one({"text": "Eid holidays from Monday"})
print("databases:", client.list_database_names())
print("collections:", db.list_collection_names())
db.notices.rename("announcements")
print("after rename:", db.list_collection_names())

# %% [markdown]
# ## Example 2 - ordered vs unordered inserts

# %%
from pymongo.errors import BulkWriteError
for ordered in (True, False):
    db.t.drop()
    try:
        db.t.insert_many([{"_id": 1}, {"_id": 1}, {"_id": 2}], ordered=ordered)
    except BulkWriteError as e:
        print(f"ordered={ordered}: inserted {e.details['nInserted']} of 3")

# %% [markdown]
# ## Example 3 - bulk writes

# %%
from pymongo import DeleteOne, InsertOne
res = db.batches.bulk_write([InsertOne({"_id": "WEB-01"}), InsertOne({"_id": "NET-01"}), DeleteOne({"_id": "NET-01"})])
print("inserted", res.inserted_count, "| deleted", res.deleted_count)

# %% [markdown]
# ## Example 4 - embedding

# %%
db.batches.insert_one({"_id": "DS-01", "faculty": {"name": "Aseef Ahmed", "subject": "Python"},
                       "slots": [{"day": "Mon", "time": "18:00"}, {"day": "Wed", "time": "18:00"}]})
print(db.batches.find_one({"_id": "DS-01"}))
print("faculty only:", db.batches.find_one({"_id": "DS-01"}, {"faculty.name": 1, "_id": 0}))

# %% [markdown]
# ## Example 5 - referencing and many-to-many

# %%
db.students.insert_many([{"student_id": 1, "name": "Ali Raza"}, {"student_id": 2, "name": "Sana Khan"}])
db.payments.insert_many([{"student_id": 2, "amount": 15000, "month": "2026-09"},
                         {"student_id": 2, "amount": 15000, "month": "2026-10"}])
db.students.update_one({"student_id": 2}, {"$set": {"course_ids": ["PY101", "DB201"]}})
db.students.update_one({"student_id": 1}, {"$set": {"course_ids": ["PY101"]}})
sana = db.students.find_one({"name": "Sana Khan"})
print("Sana paid:", sum(p["amount"] for p in db.payments.find({"student_id": sana["student_id"]})))
print("taking DB201:", [s["name"] for s in db.students.find({"course_ids": "DB201"})])

# %% [markdown]
# ## Example 6 - validating documents

# %%
from schema_check import STUDENT_SCHEMA, check
print(check({"name": "Sana Khan", "batch": "DS-01", "marks": {"python": 90}}, STUDENT_SCHEMA))
print(check({"name": "Al", "batch": "XX-9", "marks": {"python": 120}}, STUDENT_SCHEMA))
