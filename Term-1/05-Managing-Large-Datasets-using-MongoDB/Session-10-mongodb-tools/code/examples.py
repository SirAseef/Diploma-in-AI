"""Session 10 - MongoDB tools: Python equivalents (files are written to code/output/)."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Setup

# %%
from pathlib import Path
from campus_data import seed
from mongo_conn import get_client
from tools_py import (dump_collection, export_csv, export_jsonl, get_file, import_csv, import_jsonl,
                      put_file, restore_collection)
OUT = Path("output"); OUT.mkdir(exist_ok=True)
client = get_client()
db = client["campus_tools"]
for c in db.list_collection_names():
    db[c].drop()
print(seed(db))

# %% [markdown]
# ## Example 1 - dump to BSON and restore

# %%
n = dump_collection(db.students, OUT / "dump/campus/students.bson")
db_new = client["campus_restored"]; db_new.students.drop()
print("dumped", n, "| restored", restore_collection(db_new.students, OUT / "dump/campus/students.bson"))
print("file size:", (OUT / "dump/campus/students.bson").stat().st_size, "bytes")

# %% [markdown]
# ## Example 2 - Extended JSON keeps types

# %%
from bson import json_util
text = json_util.dumps(db.students.find_one({"student_id": 1}, {"_id": 0, "name": 1, "enrolled": 1}),
                       json_options=json_util.CANONICAL_JSON_OPTIONS)
print(text)
print(type(json_util.loads(text)["enrolled"]).__name__)

# %% [markdown]
# ## Example 3 - export to CSV

# %%
export_csv(db.students, OUT / "students.csv", fields=["name", "city", "marks.python", "marks.sql"])
print((OUT / "students.csv").read_text().splitlines()[:3])

# %% [markdown]
# ## Example 4 - import a CSV with type conversion

# %%
(OUT / "leads.csv").write_text("name,age,city,fee_offered\nKashif,19,Karachi,15000\nIqra,21,Hyderabad,\nNoman,20,Karachi,12500.5\n")
db.leads.drop()
import_csv(db.leads, OUT / "leads.csv", types={"age": int, "fee_offered": float})
for d in db.leads.find({}, {"_id": 0}):
    print(d)

# %% [markdown]
# ## Example 5 - store a large file in chunks

# %%
data = bytes(range(256)) * 4000                    # ~1 MB of fake PDF bytes
file_id = put_file(db, "admission_form.pdf", data)
print("chunks:", db.fs_chunks.count_documents({"files_id": file_id}))
assert get_file(db, file_id) == data

# %% [markdown]
# ## Example 6 - mini mongotop: collection sizes

# %%
for name in sorted(db.list_collection_names()):
    print(f"{name:<10} {db[name].estimated_document_count():>4} docs")
