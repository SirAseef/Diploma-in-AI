"""Session 06 - Shell methods and their PyMongo equivalents: worked examples."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Setup

# %%
from campus_data import seed
from mongo_conn import get_db
db = get_db("campus_shell")
for c in db.list_collection_names():
    db[c].drop()
print(seed(db))

# %% [markdown]
# ## Example 1 - sort, skip, limit

# %%
page1 = [(d["name"], d["marks"]["python"]) for d in
         db.students.find({}, {"_id": 0, "name": 1, "marks.python": 1}).sort("marks.python", -1).limit(3)]
page2 = [d["name"] for d in db.students.find({}, {"_id": 0, "name": 1}).sort("marks.python", -1).skip(3).limit(3)]
print(page1, page2, sep="\n")
assert page1[0][0] == "Faraz Iqbal"

# %% [markdown]
# ## Example 2 - multi-key sort

# %%
for d in db.students.find({}, {"_id": 0, "batch": 1, "name": 1, "marks.python": 1}).sort([("batch", 1), ("marks.python", -1)]):
    print(d["batch"], d["marks"]["python"], d["name"])

# %% [markdown]
# ## Example 3 - iterating a cursor manually

# %%
cur = db.students.find({"city": "Karachi"}).sort("student_id", 1)
first, second = next(cur), next(cur)
rest = [d["name"] for d in cur]
print(first["name"], "|", second["name"], "|", rest)

# %% [markdown]
# ## Example 4 - atomic find_one_and_update

# %%
from pymongo import ReturnDocument
for _ in range(3):
    counter = db.counters.find_one_and_update({"_id": "roll_no"}, {"$inc": {"seq": 1}},
                                              upsert=True, return_document=ReturnDocument.AFTER)
print("next roll number:", counter["seq"])
assert counter["seq"] == 3

# %% [markdown]
# ## Example 5 - replace_one vs update_one

# %%
db.batches.replace_one({"_id": "DS-02"}, {"programme": "Data Science", "room": 9})
db.batches.update_one({"_id": "AI-01"}, {"$set": {"room": 7}})
print(db.batches.find_one({"_id": "DS-02"}))
print(sorted(db.batches.find_one({"_id": "AI-01"}).keys()))

# %% [markdown]
# ## Example 6 - exact vs estimated counts, sibling database

# %%
print(db.students.count_documents({"batch": "DS-01"}), db.students.estimated_document_count())
shop = db.client["shop_demo"]
print("sibling db name:", shop.name)
