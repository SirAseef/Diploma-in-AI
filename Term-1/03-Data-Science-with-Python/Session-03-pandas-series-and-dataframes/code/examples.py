"""Session 03 - pandas Series and DataFrames: worked examples."""

# %% [markdown]
# ## Example 1 - a Series with labels

# %%
import pandas as pd
sales = pd.Series([1200, 950, 1430], index=["Mon", "Tue", "Wed"], name="biryani_plates")
print(sales["Tue"], sales.mean(), sales.idxmax())

# %% [markdown]
# ## Example 2 - build and inspect a DataFrame

# %%
df = pd.DataFrame({
    "name": ["Ali", "Sana", "Hamza", "Ayesha", "Bilal"],
    "city": ["Karachi", "Lahore", "Karachi", "Islamabad", "Lahore"],
    "maths": [72, 91, 48, 66, 80],
    "english": [65, 88, 55, 79, 70],
})
print(df.shape)
print(df.dtypes)
print(df.describe())

# %% [markdown]
# ## Example 3 - loc vs iloc

# %%
df = df.set_index("name")
print(df.loc["Sana", "maths"])
print(df.iloc[0:2, 1:3])
print(df.loc["Ali":"Hamza", ["maths"]])   # label slice is inclusive

# %% [markdown]
# ## Example 4 - filtering

# %%
print(df[df["maths"] >= 70])
print(df[(df["city"] == "Lahore") & (df["english"] > 75)])
print(df.query("maths < 60 or english < 60"))

# %% [markdown]
# ## Example 5 - new columns and sorting

# %%
df["total"] = df["maths"] + df["english"]
df["grade"] = df["total"].apply(lambda t: "A" if t >= 160 else "B" if t >= 130 else "C")
print(df.sort_values("total", ascending=False))
assert df.loc["Sana", "grade"] == "A"

# %% [markdown]
# ## Example 6 - column arithmetic and value counts

# %%
print("avg gap:", (df["maths"] - df["english"]).abs().mean())
print(df["city"].value_counts())
