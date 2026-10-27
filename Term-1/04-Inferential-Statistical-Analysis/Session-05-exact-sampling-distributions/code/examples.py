"""Session 05 - Exact sampling distributions: worked examples."""

# %% [markdown]
# ## Example 1 - t approaches the normal

# %%
import numpy as np
import pandas as pd
from scipy import stats
rng = np.random.default_rng(5)
for df in (2, 5, 30, 1000):
    print(f"df={df:>4}: t(0.975) = {stats.t.ppf(0.975, df):.3f}")
print("normal z(0.975) =", round(stats.norm.ppf(0.975), 3))

# %% [markdown]
# ## Example 2 - where chi-square comes from

# %%
n, sigma = 8, 5
stat = np.array([(n - 1) * rng.normal(50, sigma, n).var(ddof=1) / sigma ** 2 for _ in range(20000)])
print("mean of simulated statistic:", round(stat.mean(), 2), "(df =", n - 1, ")")
print("simulated 95th pct:", round(np.percentile(stat, 95), 2), "| chi2.ppf:", round(stats.chi2.ppf(0.95, n - 1), 2))

# %% [markdown]
# ## Example 3 - 95% CI for a variance

# %%
fills = rng.normal(500, 3, 15)
n, s2 = len(fills), fills.var(ddof=1)
lo = (n - 1) * s2 / stats.chi2.ppf(0.975, n - 1)
hi = (n - 1) * s2 / stats.chi2.ppf(0.025, n - 1)
print(f"s = {np.sqrt(s2):.2f} ml; 95% CI for sigma: ({np.sqrt(lo):.2f}, {np.sqrt(hi):.2f}) ml")

# %% [markdown]
# ## Example 4 - goodness-of-fit: is the die fair?

# %%
observed = [18, 22, 16, 25, 30, 9]
res = stats.chisquare(observed)
print(res)

# %% [markdown]
# ## Example 5 - test of independence

# %%
df = pd.DataFrame({"programme": rng.choice(["DS", "Web", "Net"], 300, p=[0.4, 0.4, 0.2])})
p_place = df["programme"].map({"DS": 0.75, "Web": 0.6, "Net": 0.45})
df["placed"] = np.where(rng.random(300) < p_place, "yes", "no")
table = pd.crosstab(df["programme"], df["placed"])
chi2, p, dof, expected = stats.chi2_contingency(table)
print(table, f"\nchi2 = {chi2:.2f}, dof = {dof}, p = {p:.4f}")
print(pd.DataFrame(expected, index=table.index, columns=table.columns).round(1))

# %% [markdown]
# ## Example 6 - F-test for equal variances

# %%
a, b = rng.normal(60, 5, 20), rng.normal(60, 10, 25)
F = a.var(ddof=1) / b.var(ddof=1)
p = 2 * min(stats.f.sf(F, len(a) - 1, len(b) - 1), stats.f.cdf(F, len(a) - 1, len(b) - 1))
print(f"F = {F:.3f}, p = {p:.4f} | Levene p = {stats.levene(a, b).pvalue:.4f}")
