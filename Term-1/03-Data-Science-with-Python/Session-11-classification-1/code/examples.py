"""Session 11 - Classification I (logistic regression, KNN): worked examples."""

# %% [markdown]
# ## Example 1 - the sigmoid

# %%
import numpy as np
import pandas as pd
z = np.array([-4, -1, 0, 1, 4])
print((1 / (1 + np.exp(-z))).round(3))

# %% [markdown]
# ## Example 2 - logistic regression: pass / fail

# %%
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
rng = np.random.default_rng(11)
n = 400
hours = rng.uniform(0, 12, n)
attendance = rng.uniform(40, 100, n)
logit = -9 + 0.7 * hours + 0.08 * attendance
y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
X = np.column_stack([hours, attendance])
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=0)
logreg = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_tr, y_tr)
print("test accuracy:", round(logreg.score(X_te, y_te), 3))
print("P(fail), P(pass) for 6 h & 85%:", logreg.predict_proba([[6, 85]]).round(3))

# %% [markdown]
# ## Example 3 - reading coefficients

# %%
coef = logreg[-1].coef_[0]
print(dict(zip(["study_hours", "attendance"], coef.round(2))))
assert (coef > 0).all()

# %% [markdown]
# ## Example 4 - changing the threshold

# %%
proba = logreg.predict_proba(X_te)[:, 1]
for t in (0.3, 0.5, 0.7):
    print(f"threshold {t}: predicted pass = {(proba >= t).sum()} of {len(proba)}")

# %% [markdown]
# ## Example 5 - KNN and the effect of k

# %%
from sklearn.neighbors import KNeighborsClassifier
for k in [1, 5, 15, 51]:
    knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k)).fit(X_tr, y_tr)
    print(f"k={k:>2}: train {knn.score(X_tr, y_tr):.3f} | test {knn.score(X_te, y_te):.3f}")

# %% [markdown]
# ## Example 6 - mixed numeric + categorical features

# %%
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
df = pd.DataFrame({"income": rng.normal(80, 25, n), "age": rng.integers(20, 60, n),
                   "city": rng.choice(["Karachi", "Lahore", "Quetta"], n)})
target = ((df["income"] > 75) ^ (rng.random(n) < 0.1)).astype(int)
pre = ColumnTransformer([("num", StandardScaler(), ["income", "age"]),
                         ("cat", OneHotEncoder(handle_unknown="ignore"), ["city"])])
model = make_pipeline(pre, LogisticRegression(max_iter=1000))
d_tr, d_te, t_tr, t_te = train_test_split(df, target, random_state=0)
print("mixed-feature accuracy:", round(model.fit(d_tr, t_tr).score(d_te, t_te), 3))
