"""Session 01 - Introduction to statistics: worked examples."""

# %% [markdown]
# ## Example 1 - mean vs median with an outlier

# %%
import numpy as np
import pandas as pd
salaries = pd.Series([45, 52, 48, 60, 55, 50, 47, 900])
print("mean", round(salaries.mean(), 1), "| median", salaries.median(), "| mode", salaries.mode().tolist()[:3])

# %% [markdown]
# ## Example 2 - spread

# %%
marks = pd.Series([55, 62, 68, 70, 71, 74, 78, 81, 85, 96])
print("range", marks.max() - marks.min())
print("IQR", marks.quantile(0.75) - marks.quantile(0.25))
print("variance", round(marks.var(), 2), "| SD", round(marks.std(), 2))

# %% [markdown]
# ## Example 3 - sample vs population SD

# %%
x = np.array([4, 8, 6, 5, 7])
print(round(np.std(x), 3), round(np.std(x, ddof=1), 3), round(pd.Series(x).std(), 3))
assert np.isclose(np.std(x, ddof=1), pd.Series(x).std())

# %% [markdown]
# ## Example 4 - coefficient of variation

# %%
rng = np.random.default_rng(1)
heights = pd.Series(rng.normal(168, 7, 500))
incomes = pd.Series(rng.lognormal(11, 0.6, 500))
print("CV height:", round(heights.std() / heights.mean(), 3), "| CV income:", round(incomes.std() / incomes.mean(), 3))

# %% [markdown]
# ## Example 5 - skewness, percentiles, z-scores

# %%
bills = pd.Series(rng.gamma(2, 3000, 1000))
print("skew", round(bills.skew(), 2))
print(bills.quantile([0.1, 0.5, 0.9]).round(0))
z = (bills - bills.mean()) / bills.std()
print("bills more than 3 SD above mean:", int((z > 3).sum()))
assert bills.mean() > bills.median()       # right skew

# %% [markdown]
# ## Example 6 - frequency table

# %%
bins = [0, 40, 50, 60, 70, 80, 101]
table = pd.cut(marks, bins, right=False).value_counts().sort_index()
freq = pd.DataFrame({"count": table, "relative": (table / table.sum()).round(2)})
freq["cumulative"] = freq["relative"].cumsum()
print(freq)
