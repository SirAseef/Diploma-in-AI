"""Session 10 - Non-linear regression: worked examples."""

# %% [markdown]
# ## Data: a curved relationship

# %%
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
rng = np.random.default_rng(10)
x = rng.uniform(-3, 3, 120)
y = 0.8 * x ** 2 - x + 2 + rng.normal(0, 0.8, 120)
X = x.reshape(-1, 1)

def rmse(a, b):
    return float(np.sqrt(mean_squared_error(a, b)))

# %% [markdown]
# ## Example 1 - a line under-fits

# %%
lin = LinearRegression().fit(X, y)
print("linear R2:", round(r2_score(y, lin.predict(X)), 3))

# %% [markdown]
# ## Example 2 - polynomial regression

# %%
poly2 = make_pipeline(PolynomialFeatures(degree=2, include_bias=False), LinearRegression()).fit(X, y)
print("quadratic R2:", round(r2_score(y, poly2.predict(X)), 3))
print("coefficients:", poly2[-1].coef_.round(2), "intercept:", round(poly2[-1].intercept_, 2))
assert r2_score(y, poly2.predict(X)) > r2_score(y, lin.predict(X))

# %% [markdown]
# ## Example 3 - choose the degree with held-out data

# %%
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)
for d in [1, 2, 3, 5, 9, 15]:
    m = make_pipeline(PolynomialFeatures(d), StandardScaler(), LinearRegression()).fit(X_tr, y_tr)
    print(f"degree {d:>2}: train RMSE {rmse(y_tr, m.predict(X_tr)):.3f} | test RMSE {rmse(y_te, m.predict(X_te)):.3f}")

# %% [markdown]
# ## Example 4 - exponential decay (phone resale value)

# %%
from scipy.optimize import curve_fit
months = np.arange(0, 37, 3)
price = 150_000 * np.exp(-0.045 * months) * rng.normal(1, 0.03, months.size)

def decay(t, a, b):
    return a * np.exp(-b * t)

(a, b), _ = curve_fit(decay, months, price, p0=[150_000, 0.05])
print(f"a = {a:,.0f}, b = {b:.4f}, value halves every {np.log(2) / b:.1f} months")
assert abs(b - 0.045) < 0.01

# %% [markdown]
# ## Example 5 - logistic growth (app users)

# %%
weeks = np.arange(0, 30)
users = 50_000 / (1 + np.exp(-0.4 * (weeks - 12))) + rng.normal(0, 800, weeks.size)

def logistic(t, L, k, t0):
    return L / (1 + np.exp(-k * (t - t0)))

(L, k, t0), _ = curve_fit(logistic, weeks, users, p0=[users.max(), 0.3, weeks.mean()])
print(f"saturation ~{L:,.0f} users, fastest growth at week {t0:.1f}")

# %% [markdown]
# ## Example 6 - straighten with logs (power law)

# %%
area = rng.uniform(500, 3000, 80)
house_price = 9000 * area ** 1.1 * rng.normal(1, 0.08, 80)
lm = LinearRegression().fit(np.log(area).reshape(-1, 1), np.log(house_price))
print("estimated exponent b:", round(lm.coef_[0], 3))
