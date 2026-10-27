"""Session 06 - Analysis of variance: worked examples."""

# %% [markdown]
# ## Example 1 - why not many t-tests?

# %%
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
for k in (1, 3, 6, 10):
    print(f"{k:>2} tests -> P(at least one false positive) = {1 - 0.95 ** k:.3f}")

# %% [markdown]
# ## Data: four teaching methods (synthetic)

# %%
rng = np.random.default_rng(6)
effects = {"lecture": 62, "flipped": 68, "project": 71, "self_paced": 63}
df = pd.DataFrame([(m, rng.normal(mu, 9)) for m, mu in effects.items() for _ in range(30)], columns=["method", "score"])
k, N = df["method"].nunique(), len(df)
print(df.groupby("method")["score"].agg(["count", "mean", "std"]).round(1))

# %% [markdown]
# ## Example 2 - ANOVA table by hand

# %%
grand = df["score"].mean()
ssb = df.groupby("method")["score"].apply(lambda g: len(g) * (g.mean() - grand) ** 2).sum()
ssw = df.groupby("method")["score"].apply(lambda g: ((g - g.mean()) ** 2).sum()).sum()
F = (ssb / (k - 1)) / (ssw / (N - k)); p = stats.f.sf(F, k - 1, N - k)
print(f"SSB {ssb:.1f}  SSW {ssw:.1f}  F {F:.2f}  p {p:.2e}")

# %% [markdown]
# ## Example 3 - scipy and statsmodels

# %%
groups = [g["score"] for _, g in df.groupby("method")]
print(stats.f_oneway(*groups))
table = sm.stats.anova_lm(smf.ols("score ~ C(method)", data=df).fit(), typ=2)
print(table)
assert np.isclose(table.loc["C(method)", "F"], F)

# %% [markdown]
# ## Example 4 - assumptions

# %%
print("Levene p:", round(stats.levene(*groups).pvalue, 3))
print("Shapiro p (residuals):", round(stats.shapiro(smf.ols("score ~ C(method)", df).fit().resid).pvalue, 3))

# %% [markdown]
# ## Example 5 - Tukey HSD and eta squared

# %%
from statsmodels.stats.multicomp import pairwise_tukeyhsd
print(pairwise_tukeyhsd(df["score"], df["method"], alpha=0.05))
print("eta squared:", round(ssb / (ssb + ssw), 3))

# %% [markdown]
# ## Example 6 - two-way ANOVA with interaction

# %%
rows = []
for fert, f_eff in {"urea": 0, "DAP": 4, "organic": 2}.items():
    for irr, i_eff in {"canal": 0, "drip": 5}.items():
        bonus = 4 if (fert == "DAP" and irr == "drip") else 0
        rows += [(fert, irr, 40 + f_eff + i_eff + bonus + rng.normal(0, 3)) for _ in range(12)]
farm = pd.DataFrame(rows, columns=["fertiliser", "irrigation", "yield_kg"])
print(sm.stats.anova_lm(smf.ols("yield_kg ~ C(fertiliser) * C(irrigation)", data=farm).fit(), typ=2).round(4))
