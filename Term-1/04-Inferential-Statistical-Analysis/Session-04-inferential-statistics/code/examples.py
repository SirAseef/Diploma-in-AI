"""Session 04 - Inferential statistics: worked examples."""

# %% [markdown]
# ## Example 1 - the Central Limit Theorem

# %%
import numpy as np
from scipy import stats
rng = np.random.default_rng(4)
population = rng.exponential(scale=5000, size=1_000_000)
means = rng.choice(population, (5000, 40)).mean(axis=1)
print("SD of sample means:", round(means.std()), "| sigma/sqrt(n):", round(population.std() / np.sqrt(40)))
print("skew population:", round(stats.skew(population), 2), "| skew of means:", round(stats.skew(means), 2))

# %% [markdown]
# ## Example 2 - a 95% CI for a mean

# %%
sample = rng.normal(72, 9, 30)
se = stats.sem(sample)
lo, hi = stats.t.interval(0.95, df=len(sample) - 1, loc=sample.mean(), scale=se)
print(f"mean {sample.mean():.1f}, SE {se:.2f}, 95% CI ({lo:.1f}, {hi:.1f})")

# %% [markdown]
# ## Example 3 - what 95% confidence means

# %%
covered = 0
for _ in range(1000):
    s = rng.normal(70, 10, 25)
    lo, hi = stats.t.interval(0.95, 24, loc=s.mean(), scale=stats.sem(s))
    covered += lo <= 70 <= hi
print("coverage:", covered / 1000)
assert 0.92 < covered / 1000 < 0.98

# %% [markdown]
# ## Example 4 - one-sample and paired t-tests

# %%
fill = rng.normal(497, 4, 25)                    # 500 ml bottles
print("one-sample:", stats.ttest_1samp(fill, popmean=500))
before = rng.normal(60, 10, 20); after = before + rng.normal(4, 5, 20)
print("paired:", stats.ttest_rel(after, before))

# %% [markdown]
# ## Example 5 - Welch two-sample t-test and effect size

# %%
campus_a, campus_b = rng.normal(68, 10, 40), rng.normal(63, 14, 45)
t, p = stats.ttest_ind(campus_a, campus_b, equal_var=False)
d = (campus_a.mean() - campus_b.mean()) / np.sqrt((campus_a.var(ddof=1) + campus_b.var(ddof=1)) / 2)
print(f"t = {t:.2f}, p = {p:.4f}, Cohen's d = {d:.2f}")

# %% [markdown]
# ## Example 6 - A/B test of two proportions

# %%
from statsmodels.stats.proportion import proportions_ztest
z, p = proportions_ztest(count=[132, 168], nobs=[2400, 2400])
print(f"sign-up rate old {132 / 2400:.3f} vs new {168 / 2400:.3f}: z = {z:.2f}, p = {p:.4f}")
