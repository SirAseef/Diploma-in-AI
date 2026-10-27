"""Session 04 - Advanced pandas: worked examples."""

# %% [markdown]
# ## Sample data: restaurant orders

# %%
import numpy as np
import pandas as pd
rng = np.random.default_rng(4)
n = 60
orders = pd.DataFrame({
    "order_id": range(1, n + 1),
    "date": pd.date_range("2026-10-01", periods=n, freq="8h").strftime("%Y-%m-%d"),
    "branch": rng.choice(["Clifton", "Gulshan", "DHA"], n),
    "channel": rng.choice(["dine-in", "delivery", "takeaway"], n),
    "amount": rng.integers(800, 4000, n),
})
print(orders.head())

# %% [markdown]
# ## Example 1 - groupby with named aggregations

# %%
summary = orders.groupby("branch").agg(
    orders=("order_id", "count"), revenue=("amount", "sum"), avg_bill=("amount", "mean")).round(0)
print(summary)
assert summary["orders"].sum() == n

# %% [markdown]
# ## Example 2 - transform

# %%
orders["branch_avg"] = orders.groupby("branch")["amount"].transform("mean")
orders["above_avg"] = orders["amount"] > orders["branch_avg"]
print(orders[["branch", "amount", "branch_avg", "above_avg"]].head())

# %% [markdown]
# ## Example 3 - pivot table and crosstab

# %%
pt = pd.pivot_table(orders, index="branch", columns="channel", values="amount", aggfunc="sum", fill_value=0)
ct = pd.crosstab(orders["branch"], orders["channel"])
print(pt, ct, sep="\n\n")
assert ct.values.sum() == n

# %% [markdown]
# ## Example 4 - merge

# %%
branches = pd.DataFrame({"branch": ["Clifton", "Gulshan", "DHA"], "manager": ["Faraz", "Hina", "Usman"]})
full = orders.merge(branches, on="branch", how="left", validate="many_to_one")
print(full[["order_id", "branch", "manager"]].head())
assert len(full) == len(orders)

# %% [markdown]
# ## Example 5 - melt and pivot

# %%
wide = pd.DataFrame({"student": ["Ali", "Sana"], "maths": [72, 91], "physics": [65, 88]})
long = wide.melt(id_vars="student", var_name="subject", value_name="marks")
back = long.pivot(index="student", columns="subject", values="marks")
print(long, back, sep="\n\n")

# %% [markdown]
# ## Example 6 - dates, resample, rolling

# %%
orders["date"] = pd.to_datetime(orders["date"])
daily = orders.set_index("date")["amount"].resample("D").sum()
print(daily.head())
print(daily.resample("W").sum())
print(daily.rolling(3).mean().round(0).head())
