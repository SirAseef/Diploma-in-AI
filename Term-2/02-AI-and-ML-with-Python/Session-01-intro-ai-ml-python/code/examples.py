"""Session 01 - Introduction to AI and ML with Python: worked examples."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - a synthetic student dataset with mixed types

# %%
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

NUM, CAT = ["attendance", "quiz_avg"], ["city", "shift"]


def make_students(n=500, seed=21):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({"attendance": rng.uniform(40, 100, n).round(0),
                       "quiz_avg": rng.uniform(0, 20, n).round(1),
                       "city": rng.choice(["Karachi", "Lahore", "Islamabad"], n),
                       "shift": rng.choice(["morning", "evening"], n, p=[0.6, 0.4])})
    logit = 0.06 * (df.attendance - 70) + 0.3 * (df.quiz_avg - 10) + 0.4 * (df["shift"] == "morning")
    df["passed"] = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    df.loc[rng.choice(n, 30, replace=False), "quiz_avg"] = np.nan
    return df


df = make_students()
print(df.head()); print(df.isna().sum().to_dict())

# %% [markdown]
# ## Example 2 - preprocessing with ColumnTransformer

# %%
pre = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), NUM),
    ("cat", OneHotEncoder(handle_unknown="ignore"), CAT)])
X, y = df[NUM + CAT], df["passed"]
print("transformed shape:", pre.fit_transform(X).shape)

# %% [markdown]
# ## Example 3 - a full pipeline

# %%
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
pipe = Pipeline([("pre", pre), ("model", LogisticRegression(max_iter=1000))])
pipe.fit(X_tr, y_tr)
print("test accuracy:", round(pipe.score(X_te, y_te), 3))

# %% [markdown]
# ## Example 4 - cross-validation

# %%
scores = cross_val_score(pipe, X, y, cv=5)
print("CV scores:", scores.round(3), "mean:", scores.mean().round(3), "std:", scores.std().round(3))

# %% [markdown]
# ## Example 5 - comparing models fairly

# %%
cands = {"logreg": LogisticRegression(max_iter=1000), "tree": DecisionTreeClassifier(max_depth=4, random_state=0),
         "forest": RandomForestClassifier(200, random_state=0)}
for name, m in cands.items():
    print(f"{name:7s}", cross_val_score(Pipeline([("pre", pre), ("model", m)]), X, y, cv=5).mean().round(3))

# %% [markdown]
# ## Example 6 - save and reload with joblib

# %%
os.makedirs("output", exist_ok=True)
joblib.dump(pipe, "output/pass_model.joblib")
loaded = joblib.load("output/pass_model.joblib")
new = pd.DataFrame({"attendance": [92, 55], "quiz_avg": [16, np.nan], "city": ["Karachi", "Quetta"],
                    "shift": ["morning", "evening"]})
print("pass probability:", loaded.predict_proba(new)[:, 1].round(3))
