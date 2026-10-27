"""Session 11 - MongoDB Atlas: connection strings, secrets, retries and search ideas (runs offline)."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - build a connection string with an encoded password

# %%
from atlas_helpers import best_region, build_uri, connect_with_retry, describe_uri, fuzzy_search, mask
uri = build_uri("report_bot", "P@ss:w0rd/2026", "cluster0.abcde.mongodb.net", db="campus", app="campus-portal")
print(uri)

# %% [markdown]
# ## Example 2 - inspect a URI and mask the password

# %%
info = describe_uri(uri)
print(info["host"], info["db"], info["options"])
print(mask(uri))
assert "P%40ss" not in mask(uri)

# %% [markdown]
# ## Example 3 - read the URI from the environment

# %%
import os
from mongo_conn import backend
print("MONGO_URI set?", bool(os.environ.get("MONGO_URI")), "| scripts will use:", backend())

# %% [markdown]
# ## Example 4 - connect with retry and back-off

# %%
attempts = {"n": 0}
waits = []

def flaky_factory():
    attempts["n"] += 1
    if attempts["n"] < 3:
        raise ConnectionError("cluster still waking up")
    return "connected client"

print(connect_with_retry(flaky_factory, attempts=4, base_delay=0.5, sleep=waits.append), "after", attempts["n"], "tries; waits:", waits)

# %% [markdown]
# ## Example 5 - choose a region by latency

# %%
print(best_region({"ap-south-1 (Mumbai)": 48, "me-south-1 (Bahrain)": 39, "eu-west-1 (Ireland)": 160}))

# %% [markdown]
# ## Example 6 - fuzzy matching (the idea behind Atlas Search)

# %%
from campus_data import student_docs
print(fuzzy_search(student_docs(), "pyton", fields=["skills"])[:3])
print(fuzzy_search(student_docs(), "Ayesa", fields=["name"], threshold=0.5)[:2])
