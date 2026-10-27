"""Session 01 - Introduction to MongoDB: worked examples (mongomock by default; set MONGO_URI for a real server)."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - connect, insert, find

# %%
from mongo_conn import backend, get_db
print("Backend:", backend())
db = get_db("campus_intro")
db.students.drop(); db.payments.drop()
res = db.students.insert_one({"name": "Ali Raza", "city": "Karachi", "marks": {"python": 78}})
print("inserted _id:", res.inserted_id)
print(db.students.find_one({"name": "Ali Raza"}))

# %% [markdown]
# ## Example 2 - flexible schema

# %%
db.students.insert_many([
    {"name": "Sana Khan", "city": "Lahore", "skills": ["python", "sql"]},
    {"name": "Hamza Ali", "phone": "0300-1234567"},
])
for d in db.students.find({}, {"_id": 0}):
    print(d)

# %% [markdown]
# ## Example 3 - what's inside an ObjectId

# %%
oid = res.inserted_id
print(type(oid).__name__, str(oid), "| created:", oid.generation_time)

# %% [markdown]
# ## Example 4 - BSON types from Python

# %%
from datetime import datetime
from bson.decimal128 import Decimal128
db.payments.insert_one({"amount": Decimal128("15000.50"), "paid_on": datetime(2026, 10, 27), "late": False})
p = db.payments.find_one({}, {"_id": 0})
print({k: (type(v).__name__, str(v)) for k, v in p.items()})

# %% [markdown]
# ## Example 5 - count, distinct, update, delete

# %%
print("Karachi:", db.students.count_documents({"city": "Karachi"}))
print("cities:", db.students.distinct("city"))
db.students.update_one({"name": "Hamza Ali"}, {"$set": {"city": "Karachi"}})
print("Karachi after update:", db.students.count_documents({"city": "Karachi"}))
db.students.delete_many({"city": {"$exists": False}})
print("total now:", db.students.count_documents({}))

# %% [markdown]
# ## Example 6 - SQL vs MongoDB

# %%
# SELECT name FROM students WHERE city = 'Karachi' ORDER BY name;
print(list(db.students.find({"city": "Karachi"}, {"_id": 0, "name": 1}).sort("name", 1)))
