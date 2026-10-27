"""Session 15 - Regression Techniques for Machine Learning: worked examples."""

# %% [markdown]
# ## Example 1 - simple linear regression, by formula and with scikit-learn

# %%
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

hours = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float)
marks = np.array([35, 42, 50, 54, 61, 68, 73, 82], dtype=float)
m = ((hours - hours.mean()) * (marks - marks.mean())).sum() / ((hours - hours.mean()) ** 2).sum()
c = marks.mean() - m * hours.mean()
print(f"by formula: marks = {m:.2f} * hours + {c:.2f}")
lr = LinearRegression().fit(hours.reshape(-1, 1), marks)
print(f"sklearn   : marks = {lr.coef_[0]:.2f} * hours + {lr.intercept_:.2f}")
print("9 hours ->", lr.predict([[9]]).round(1))

# %% [markdown]
# ## Example 2 - evaluation metrics: MAE, MSE, RMSE, R²

# %%
pred = lr.predict(hours.reshape(-1, 1))
mae = mean_absolute_error(marks, pred); mse = mean_squared_error(marks, pred)
print(f"MAE {mae:.2f} | MSE {mse:.2f} | RMSE {np.sqrt(mse):.2f} | R² {r2_score(marks, pred):.3f}")

# %% [markdown]
# ## Example 3 - multiple linear regression: flat prices in Karachi

# %%
rng = np.random.default_rng(0)
n = 300
flats = pd.DataFrame({
    "sqft": rng.integers(600, 2500, n),
    "bedrooms": rng.integers(1, 5, n),
    "age_years": rng.integers(0, 30, n),
    "floor": rng.integers(0, 12, n),
})
flats["price_lakh"] = (0.06 * flats.sqft + 8 * flats.bedrooms - 1.2 * flats.age_years
                       + 0.8 * flats.floor + 20 + rng.normal(0, 10, n)).round(1)
X, y = flats.drop(columns="price_lakh"), flats["price_lakh"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0)
mlr = LinearRegression().fit(X_tr, y_tr)
print(pd.Series(mlr.coef_, index=X.columns).round(3))
print("test R²:", round(r2_score(y_te, mlr.predict(X_te)), 3))

# %% [markdown]
# ## Example 4 - polynomial regression for curved data

# %%
x = np.sort(rng.uniform(0, 10, 40)); yc = 2 + 1.5 * x - 0.12 * x**2 + rng.normal(0, 0.6, 40)
Xc = x.reshape(-1, 1)
folds = KFold(n_splits=5, shuffle=True, random_state=0)     # shuffle: x is sorted!
for d in [1, 2, 10]:
    model = make_pipeline(PolynomialFeatures(d), StandardScaler(), LinearRegression())
    cv = cross_val_score(model, Xc, yc, cv=folds, scoring="r2").mean()
    print(f"degree {d:2d}: train R² {model.fit(Xc, yc).score(Xc, yc):.3f} | cross-validated R² {cv:.3f}")

# %% [markdown]
# ## Example 5 - regularization: Ridge (L2) and Lasso (L1)

# %%
noise = pd.DataFrame(rng.normal(size=(n, 10)), columns=[f"noise{i}" for i in range(10)])
Xn = pd.concat([X, noise], axis=1)
Xn_tr, Xn_te, yn_tr, yn_te = train_test_split(Xn, y, test_size=0.2, random_state=0)
for name, model in [("Linear", LinearRegression()), ("Ridge", Ridge(alpha=10)), ("Lasso", Lasso(alpha=1.0))]:
    pipe = make_pipeline(StandardScaler(), model).fit(Xn_tr, yn_tr)
    coefs = pipe[-1].coef_
    print(f"{name:6s} test R² {pipe.score(Xn_te, yn_te):.3f} | zeroed coefficients: {(np.abs(coefs) < 1e-6).sum()}")

# %% [markdown]
# ## Example 6 - a non-linear model: random forest regressor

# %%
rf = RandomForestRegressor(n_estimators=200, random_state=0).fit(X_tr, y_tr)
print("random forest test R²:", round(rf.score(X_te, y_te), 3))
print(pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False).round(3))
