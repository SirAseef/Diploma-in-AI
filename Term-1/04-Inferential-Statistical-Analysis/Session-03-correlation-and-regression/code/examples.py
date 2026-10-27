"""Session 03 - Correlation and regression: worked examples."""

# %% [markdown]
# ## Data: students (synthetic)

# %%
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
rng = np.random.default_rng(3)
n = 200
df = pd.DataFrame({"attendance": rng.uniform(50, 100, n).round(0), "study_hours": rng.uniform(0, 15, n).round(1),
                   "campus": rng.choice(["North", "South"], n)})
df["marks"] = (5 + 0.5 * df["attendance"] + 1.8 * df["study_hours"] + (df["campus"] == "North") * 3
               + rng.normal(0, 6, n)).round(1)
x, y = df["attendance"].to_numpy(), df["marks"].to_numpy()

# %% [markdown]
# ## Example 1 - covariance and Pearson r by hand

# %%
cov = ((x - x.mean()) * (y - y.mean())).sum() / (len(x) - 1)
r = cov / (x.std(ddof=1) * y.std(ddof=1))
r_scipy, p = stats.pearsonr(x, y)
print(f"cov {cov:.2f} | r {r:.3f} | scipy r {r_scipy:.3f}, p = {p:.2e}")
assert np.isclose(r, r_scipy)

# %% [markdown]
# ## Example 2 - Pearson vs Spearman with an outlier

# %%
xs, ys = x[:30], y[:30]
x2, y2 = np.append(xs, 40), np.append(ys, 150)
print("Pearson:", round(stats.pearsonr(xs, ys)[0], 3), "->", round(stats.pearsonr(x2, y2)[0], 3))
print("Spearman:", round(stats.spearmanr(xs, ys)[0], 3), "->", round(stats.spearmanr(x2, y2)[0], 3))

# %% [markdown]
# ## Example 3 - zero correlation, strong relationship

# %%
u = np.linspace(-3, 3, 100); v = u ** 2
print("r(u, u^2) =", round(stats.pearsonr(u, v)[0], 6))

# %% [markdown]
# ## Example 4 - simple regression with linregress

# %%
res = stats.linregress(df["attendance"], df["marks"])
print(f"marks = {res.intercept:.2f} + {res.slope:.3f} * attendance | R2 = {res.rvalue ** 2:.3f} | p = {res.pvalue:.2e}")

# %% [markdown]
# ## Example 5 - statsmodels table and intervals

# %%
model = smf.ols("marks ~ attendance", data=df).fit()
print(model.summary().tables[1])
print(model.conf_int().round(3))
print(model.get_prediction(pd.DataFrame({"attendance": [90]})).summary_frame(alpha=0.05).round(2))

# %% [markdown]
# ## Example 6 - multiple regression and residuals

# %%
m2 = smf.ols("marks ~ attendance + study_hours + C(campus)", data=df).fit()
print(m2.params.round(3)); print("adj R2:", round(m2.rsquared_adj, 3))
print("Shapiro p-value of residuals:", round(stats.shapiro(m2.resid).pvalue, 3))
assert m2.rsquared_adj > model.rsquared_adj
