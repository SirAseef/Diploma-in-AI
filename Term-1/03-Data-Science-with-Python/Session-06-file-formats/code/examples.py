"""Session 06 - Handling different file formats: worked examples (files go to code/output/)."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Setup

# %%
import io
from pathlib import Path
import numpy as np
import pandas as pd
OUT = Path("output"); OUT.mkdir(exist_ok=True)

# %% [markdown]
# ## Example 1 - CSV with tricky options

# %%
text = "date;phone;city;amount\n05/10/2026;03001234567;Karachi;1,200\n06/10/2026;03219876543;Quetta;-\n"
df = pd.read_csv(io.StringIO(text), sep=";", dtype={"phone": str}, parse_dates=["date"],
                 dayfirst=True, thousands=",", na_values=["-"])
print(df, df.dtypes, sep="\n")
assert df.loc[0, "phone"].startswith("0") and df.loc[0, "date"].month == 10 and df["amount"].isna().sum() == 1

# %% [markdown]
# ## Example 2 - Excel with two sheets

# %%
north = pd.DataFrame({"branch": ["Nazimabad", "Gulberg"], "sales": [120, 95]})
south = pd.DataFrame({"branch": ["Clifton", "Korangi"], "sales": [150, 80]})
with pd.ExcelWriter(OUT / "branches.xlsx") as xw:
    north.to_excel(xw, sheet_name="North", index=False)
    south.to_excel(xw, sheet_name="South", index=False)
sheets = pd.read_excel(OUT / "branches.xlsx", sheet_name=None)
print(list(sheets), pd.concat(sheets, names=["region"]).reset_index(level=0), sep="\n")

# %% [markdown]
# ## Example 3 - nested JSON

# %%
data = [{"id": 1, "user": {"name": "Ali", "city": "Karachi"}, "tags": ["ai", "python"]},
        {"id": 2, "user": {"name": "Sana", "city": "Lahore"}, "tags": ["sql"]}]
flat = pd.json_normalize(data)
print(flat)
print(flat.explode("tags"))

# %% [markdown]
# ## Example 4 - XML

# %%
xml = """<stations>
  <station id="1"><name>Saddar</name><temp>34</temp></station>
  <station id="2"><name>Malir</name><temp>36</temp></station>
</stations>"""
st = pd.read_xml(io.StringIO(xml), xpath="//station")
print(st)

# %% [markdown]
# ## Example 5 - Parquet keeps types

# %%
sales = pd.DataFrame({"date": pd.date_range("2026-10-01", periods=4),
                      "city": pd.Categorical(["Karachi", "Lahore", "Karachi", "Multan"]),
                      "amount": [1200.0, 950.5, 1430.0, 800.0]})
sales.to_parquet(OUT / "sales.parquet")
sales.to_csv(OUT / "sales.csv", index=False)
print(pd.read_parquet(OUT / "sales.parquet").dtypes)
print(pd.read_csv(OUT / "sales.csv").dtypes)   # dates and categories become plain text

# %% [markdown]
# ## Example 6 - a big file in chunks

# %%
rng = np.random.default_rng(6)
big = pd.DataFrame({"city": rng.choice(["Karachi", "Lahore", "Peshawar"], 20_000),
                    "amount": rng.integers(100, 1000, 20_000)})
big.to_csv(OUT / "big.csv", index=False)
total = 0
for chunk in pd.read_csv(OUT / "big.csv", chunksize=5_000):
    total += chunk.loc[chunk["city"] == "Karachi", "amount"].sum()
print("Karachi total:", total)
assert total == big.loc[big["city"] == "Karachi", "amount"].sum()
