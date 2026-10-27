"""Session 11 - Data Handling Using Pandas: worked examples.
Files are written into code/output/ (ignored by git)."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - create and inspect

# %%
from pathlib import Path
import pandas as pd
OUT = Path("output"); OUT.mkdir(exist_ok=True)

s = pd.Series([72, 91, 64], index=["Ali", "Sana", "Omar"], name="marks")
print(s, "\nmean:", s.mean())

df = pd.DataFrame({
    "name": ["Ayesha", "Bilal", "Hira", "Omar", "Zara", "Hamza"],
    "city": ["Karachi", "Lahore", "Karachi", "Quetta", "Lahore", "Karachi"],
    "python": [88, 64, 92, None, 75, 58],
    "sql": [79, 70, 95, 60, None, 66],
})
print(df.shape)
print(df.dtypes)
print(df.describe().round(1))

# %% [markdown]
# ## Example 2 - select and filter

# %%
print(df.loc[df["city"] == "Karachi", ["name", "python"]])
print(df.iloc[:2])
print(df.query("python >= 75 and sql >= 75"))
print(df[df["city"].isin(["Lahore", "Quetta"])]["name"].tolist())

# %% [markdown]
# ## Example 3 - handle missing values

# %%
print(df.isna().sum())
df["python"] = df["python"].fillna(df["python"].mean())
df = df.dropna(subset=["sql"]).reset_index(drop=True)
print(df)

# %% [markdown]
# ## Example 4 - new columns, apply and sort

# %%
df["total"] = df["python"] + df["sql"]
df["grade"] = df["total"].apply(lambda t: "A" if t >= 160 else "B" if t >= 130 else "C")
print(df.sort_values("total", ascending=False))

# %% [markdown]
# ## Example 5 - groupby and pivot tables

# %%
print(df.groupby("city")["total"].agg(["count", "mean", "max"]).round(1))
print(pd.pivot_table(df, values="total", index="city", columns="grade", aggfunc="count", fill_value=0))

# %% [markdown]
# ## Example 6 - merge two tables

# %%
fees = pd.DataFrame({"name": ["Ayesha", "Hira", "Omar"], "fee_paid": [True, True, False]})
print(df.merge(fees, on="name", how="left"))

# %% [markdown]
# ## Example 7 - save and reload

# %%
df.to_csv(OUT / "students.csv", index=False)
back = pd.read_csv(OUT / "students.csv")
print(back.equals(df), back.columns.tolist())
