"""Session 07 - Cleaning imported data: worked examples."""

# %% [markdown]
# ## Example 1 - inspect a messy survey

# %%
import numpy as np
import pandas as pd
raw = pd.DataFrame({
    " Name ": ["Ali", "sana ", "Hamza", "Ali", None, "Zoya"],
    "City": ["khi", "Lahore", "KARACHI ", "khi", "Isb", "lahore"],
    "Age": ["21", "abc", "19", "21", "230", "22"],
    "Fee (Rs)": ["Rs. 12,000", "15000", None, "Rs. 12,000", "9,500", None],
})
print(raw.isna().sum())
print("duplicates:", raw.duplicated().sum())

# %% [markdown]
# ## Example 2 - tidy column names and types

# %%
df = raw.rename(columns=lambda c: c.strip().lower().replace(" (rs)", "").replace(" ", "_"))
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df["fee"] = pd.to_numeric(df["fee"].str.replace(r"[^0-9.]", "", regex=True), errors="coerce")
print(df.dtypes)

# %% [markdown]
# ## Example 3 - clean text and categories

# %%
df["name"] = df["name"].str.strip().str.title()
city_map = {"khi": "Karachi", "karachi": "Karachi", "isb": "Islamabad", "lahore": "Lahore"}
df["city"] = df["city"].str.strip().str.lower().map(city_map)
print(df)

# %% [markdown]
# ## Example 4 - impossible values, duplicates, missing

# %%
df.loc[~df["age"].between(10, 80), "age"] = np.nan
df = df.drop_duplicates().dropna(subset=["name"]).copy()
df["age"] = df["age"].fillna(df["age"].median())
df["fee"] = df["fee"].fillna(df.groupby("city")["fee"].transform("median"))
print(df)

# %% [markdown]
# ## Example 5 - outliers with IQR and z-score

# %%
rng = np.random.default_rng(7)
s = pd.Series(np.append(rng.normal(50, 5, 200), [95, 4]))
q1, q3 = s.quantile([0.25, 0.75]); iqr = q3 - q1
iqr_out = s[(s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)]
z = (s - s.mean()) / s.std()
print("IQR outliers:", iqr_out.round(1).tolist())
print("z>3 outliers:", s[z.abs() > 3].round(1).tolist())
capped = s.clip(q1 - 1.5 * iqr, q3 + 1.5 * iqr)
print("max before/after capping:", round(s.max(), 1), round(capped.max(), 1))

# %% [markdown]
# ## Example 6 - validate

# %%
assert df["name"].notna().all()
assert df["age"].between(10, 80).all()
assert set(df["city"].dropna()) <= {"Karachi", "Lahore", "Islamabad"}
assert not df.duplicated().any()
print("Clean data passed all checks")
