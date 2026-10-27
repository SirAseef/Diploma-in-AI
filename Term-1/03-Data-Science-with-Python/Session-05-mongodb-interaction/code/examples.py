"""Session 05 - MongoDB interaction from Python: worked examples.
Runs on mongomock by default; set MONGO_URI to use a real MongoDB server."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - connect and insert

# %%
from mongo_conn import get_db, backend
print("Backend:", backend())
db = get_db("shop_demo")
db.orders.delete_many({})
db.orders.insert_many([
    {"customer": "Ali", "city": "Karachi", "items": [{"name": "kurta", "qty": 2, "price": 2500}], "status": "paid"},
    {"customer": "Sana", "city": "Lahore", "items": [{"name": "shawl", "qty": 1, "price": 4200}], "status": "pending"},
    {"customer": "Hina", "city": "Karachi", "items": [{"name": "kurta", "qty": 1, "price": 2600},
                                                       {"name": "dupatta", "qty": 3, "price": 900}], "status": "paid"},
])
print(db.orders.count_documents({}), "documents")

# %% [markdown]
# ## Example 2 - filters and projections

# %%
for doc in db.orders.find({"city": "Karachi"}, {"_id": 0, "customer": 1, "status": 1}):
    print(doc)

# %% [markdown]
# ## Example 3 - nested fields and arrays

# %%
print([d["customer"] for d in db.orders.find({"items.name": "kurta"})])
print([d["customer"] for d in db.orders.find({"items.qty": {"$gte": 2}})])

# %% [markdown]
# ## Example 4 - update and count

# %%
res = db.orders.update_many({"status": "pending"}, {"$set": {"status": "paid"}})
print("modified:", res.modified_count, "| paid:", db.orders.count_documents({"status": "paid"}))

# %% [markdown]
# ## Example 5 - aggregation: revenue per city

# %%
pipeline = [
    {"$unwind": "$items"},
    {"$group": {"_id": "$city", "revenue": {"$sum": {"$multiply": ["$items.qty", "$items.price"]}}}},
    {"$sort": {"revenue": -1}},
]
result = list(db.orders.aggregate(pipeline))
print(result)
assert result[0] == {"_id": "Karachi", "revenue": 10300}

# %% [markdown]
# ## Example 6 - into pandas

# %%
import pandas as pd
df = pd.json_normalize(list(db.orders.find({}, {"_id": 0})), record_path="items",
                       meta=["customer", "city", "status"])
df["line_total"] = df["qty"] * df["price"]
print(df)
print(df.groupby("name")["line_total"].sum())
