"""Session 01 - Real-life problem: same-day purchase prediction for a phone shop chain."""
# notebook: run-in-code-dir
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUM, CAT = ["age", "budget_pkr"], ["brand_pref", "visited_before", "city"]


def make_customers(n=800, seed=11):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({"age": rng.integers(16, 60, n),
                       "budget_pkr": rng.normal(60000, 25000, n).clip(15000).round(-3),
                       "brand_pref": rng.choice(["Samsung", "Infinix", "Apple", "Tecno"], n),
                       "visited_before": rng.choice(["yes", "no"], n),
                       "city": rng.choice(["Karachi", "Lahore", "Multan"], n)})
    logit = (df.budget_pkr - 60000) / 20000 + 1.2 * (df.visited_before == "yes") - 0.6 + \
        0.8 * ((df.brand_pref == "Apple") & (df.budget_pkr > 90000)) - 0.02 * (df.age - 30)
    df["bought"] = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    df.loc[rng.choice(n, 50, replace=False), "budget_pkr"] = np.nan
    return df


def build(seed=0):
    pre = ColumnTransformer([("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), NUM),
                             ("cat", OneHotEncoder(handle_unknown="ignore"), CAT)])
    cands = {"logreg": LogisticRegression(max_iter=1000), "forest": RandomForestClassifier(200, random_state=seed)}
    df = make_customers(); X, y = df[NUM + CAT], df.bought
    cv = {k: cross_val_score(Pipeline([("pre", pre), ("m", m)]), X, y, cv=5).mean() for k, m in cands.items()}
    winner = max(cv, key=cv.get)
    best = Pipeline([("pre", pre), ("m", cands[winner])]).fit(X, y)
    return cv, winner, best


if __name__ == "__main__":
    cv, winner, best = build()
    print({k: round(float(v), 3) for k, v in cv.items()}, "winner:", winner)
    os.makedirs("output", exist_ok=True); path = "output/buy_model.joblib"
    joblib.dump(best, path)
    new = pd.DataFrame({"age": [25, 45], "budget_pkr": [120000, np.nan], "brand_pref": ["Apple", "Tecno"],
                        "visited_before": ["yes", "no"], "city": ["Karachi", "Hyderabad"]})
    proba = joblib.load(path).predict_proba(new)[:, 1]
    print("buy probability:", proba.round(3))
    assert max(cv.values()) > 0.65
    assert proba[0] > proba[1]
    print("OK")
