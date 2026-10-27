"""Session 08 - Replication and sharding: simulated examples."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - majority and elections

# %%
import random
from cluster_sim import ReplicaSet, hashed_router, ranged_router, route_counts, score_key, shards_for_query
rs = ReplicaSet(["db1", "db2", "db3"])
print("majority needed:", rs.majority(), "| primary:", rs.primary)
rs.fail("db1")
print("db1 down -> new primary:", rs.elect())
rs.fail("db2")
print("db2 down too -> primary:", rs.elect(), "| can write?", rs.can_write())

# %% [markdown]
# ## Example 2 - write concern

# %%
rs = ReplicaSet(["db1", "db2", "db3"])
print(rs.write({"x": 1}, w=1), rs.write({"x": 2}, w="majority"))
rs.fail("db3")
print("one secondary down, majority still ok:", rs.write({"x": 3}, w="majority"))
try:
    rs.write({"x": 4}, w=3)
except TimeoutError as e:
    print("w=3:", e)

# %% [markdown]
# ## Example 3 - ranged sharding with a monotonic key

# %%
existing_max = 900_000
new_ids = range(existing_max, existing_max + 30_000)
print("ranged:", route_counts(new_ids, ranged_router([300_000, 600_000])))

# %% [markdown]
# ## Example 4 - hashed sharding spreads writes

# %%
print("hashed:", route_counts(new_ids, hashed_router(3)))

# %% [markdown]
# ## Example 5 - targeted vs scatter-gather

# %%
print(shards_for_query({"customer_id": 42}, key="customer_id"))
print(shards_for_query({"city": "Karachi"}, key="customer_id"))

# %% [markdown]
# ## Example 6 - scoring shard-key candidates

# %%
rng = random.Random(8)
orders = [{"city": rng.choices(["Karachi", "Lahore", "Islamabad", "Peshawar", "Quetta"], [60, 20, 10, 6, 4])[0],
           "customer_id": rng.randrange(500_000)} for _ in range(20_000)]
print(score_key(orders, "city"), score_key(orders, "customer_id"), sep="\n")
