"""Session 05 - Database commands: worked examples (emulated on mongomock, real on a server)."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Setup

# %%
from campus_data import seed
from commands import run
from mongo_conn import backend, get_db
print("Backend:", backend())
db = get_db("campus_cmds")
for c in db.list_collection_names():
    db[c].drop()
print(seed(db))

# %% [markdown]
# ## Example 1 - health check

# %%
print(run(db, "ping"), run(db, "buildInfo")["version"])

# %% [markdown]
# ## Example 2 - database statistics

# %%
stats = run(db, "dbStats")
print({k: stats[k] for k in ("collections", "objects", "dataSize", "avgObjSize", "indexes")})

# %% [markdown]
# ## Example 3 - collection statistics

# %%
cs = run(db, "collStats", "students")
print(cs["count"], "docs,", cs["size"], "bytes, avg", cs["avgObjSize"], "bytes")
assert cs["count"] == 10

# %% [markdown]
# ## Example 4 - metadata

# %%
print([c["name"] for c in run(db, "listCollections")["cursor"]["firstBatch"]])

# %% [markdown]
# ## Example 5 - count and distinct as commands

# %%
print(run(db, "count", "students", query={"city": "Karachi"})["n"])
print(run(db, "distinct", "students", key="batch")["values"])

# %% [markdown]
# ## Example 6 - a simple capacity report

# %%
for name in sorted(db.list_collection_names()):
    c = run(db, "collStats", name)
    print(f"{name:<10} {c['count']:>4} docs  {c['size']:>6} bytes")
