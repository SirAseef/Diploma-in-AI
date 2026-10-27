"""Session 07 - Indexing: worked examples."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Setup

# %%
from campus_data import seed
from mongo_conn import get_db
db = get_db("campus_idx")
for c in db.list_collection_names():
    db[c].drop()
print(seed(db))

# %% [markdown]
# ## Example 1 - create and list indexes

# %%
db.students.create_index("city")
db.students.create_index([("batch", 1), ("marks.python", -1)], name="batch_python")
db.students.create_index("skills")                        # multikey (array field)
print(list(db.students.index_information()))

# %% [markdown]
# ## Example 2 - unique index blocks duplicates

# %%
from pymongo.errors import DuplicateKeyError
db.users.create_index("email", unique=True)
db.users.insert_one({"email": "ali@campus.pk"})
try:
    db.users.insert_one({"email": "ali@campus.pk"})
except DuplicateKeyError:
    print("duplicate email rejected")

# %% [markdown]
# ## Example 3 - COLLSCAN vs IXSCAN (simulated)

# %%
import random
from index_sim import build_index, collscan, ixscan
rng = random.Random(7)
people = [{"cnic": f"42101-{rng.randrange(10**7):07d}-{rng.randrange(10)}"} for _ in range(100_000)]
target = people[54_321]["cnic"]
print(collscan(people, "cnic", target))
idx = build_index(people, "cnic")
res = ixscan(idx, target)
print({k: res[k] for k in ("stage", "examined", "returned")})

# %% [markdown]
# ## Example 4 - partial and TTL indexes

# %%
db.students.create_index("phone", name="phone_partial", partialFilterExpression={"phone": {"$exists": True}})
db.sessions.create_index("created_at", expireAfterSeconds=1800)
print(db.sessions.index_information()["created_at_1"])

# %% [markdown]
# ## Example 5 - ESR rule with a hint

# %%
db.students.create_index([("batch", 1), ("enrolled", -1), ("marks.python", 1)], name="esr")
q = db.students.find({"batch": "DS-01", "marks.python": {"$gte": 60}}, {"_id": 0, "name": 1}).sort("enrolled", -1).hint("esr")
print([d["name"] for d in q])

# %% [markdown]
# ## Example 6 - dropping an index

# %%
db.students.drop_index("batch_python")
print(list(db.students.index_information()))
