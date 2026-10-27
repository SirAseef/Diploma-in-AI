"""Session 02 - Probability: worked examples."""

# %% [markdown]
# ## Example 1 - classical vs simulated probability

# %%
import numpy as np
from scipy import stats
rng = np.random.default_rng(2)
rolls = rng.integers(1, 7, 100_000)
print("P(even) simulated:", (rolls % 2 == 0).mean(), "| exact:", 3 / 6)

# %% [markdown]
# ## Example 2 - addition rule with a contingency table

# %%
import pandas as pd
table = pd.DataFrame({"smoker": [30, 10], "non_smoker": [70, 90]}, index=["male", "female"])
total = table.values.sum()
p_male, p_smoker = table.loc["male"].sum() / total, table["smoker"].sum() / total
p_both = table.loc["male", "smoker"] / total
print("P(male or smoker) =", p_male + p_smoker - p_both)

# %% [markdown]
# ## Example 3 - conditional probability and independence

# %%
p_smoker_given_male = table.loc["male", "smoker"] / table.loc["male"].sum()
print("P(smoker | male) =", p_smoker_given_male, "vs P(smoker) =", p_smoker)
print("independent?", np.isclose(p_smoker_given_male, p_smoker))

# %% [markdown]
# ## Example 4 - Bayes: a positive dengue test

# %%
prior, sens, spec = 0.02, 0.95, 0.90
p_pos = sens * prior + (1 - spec) * (1 - prior)
posterior = sens * prior / p_pos
print(f"P(dengue | positive) = {posterior:.3f}")
sick = rng.random(1_000_000) < prior
positive = np.where(sick, rng.random(sick.size) < sens, rng.random(sick.size) > spec)
print("simulated:", round(sick[positive].mean(), 3))
assert abs(sick[positive].mean() - posterior) < 0.01

# %% [markdown]
# ## Example 5 - binomial and Poisson

# %%
print("P(>3 defective of 20, p=0.1):", round(stats.binom(n=20, p=0.1).sf(3), 4))
print("P(0 calls | 4 per minute):", round(stats.poisson(mu=4).pmf(0), 4))
print("binomial mean & var:", stats.binom(20, 0.1).mean(), stats.binom(20, 0.1).var())

# %% [markdown]
# ## Example 6 - normal distribution

# %%
heights = stats.norm(loc=168, scale=7)
print("P(160 < H < 180):", round(heights.cdf(180) - heights.cdf(160), 4))
print("95th percentile:", round(heights.ppf(0.95), 1))
print("within 1, 2, 3 SD:", [round(heights.cdf(168 + k * 7) - heights.cdf(168 - k * 7), 4) for k in (1, 2, 3)])
