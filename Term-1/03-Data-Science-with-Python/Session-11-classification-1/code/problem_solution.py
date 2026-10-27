"""Session 11 - Real-life problem: microfinance loan pre-screening."""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUM = ["monthly_income", "existing_loans", "age", "years_in_business"]
CAT = ["city"]


def make_applicants(n=1500, seed=5):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "monthly_income": rng.gamma(4, 15_000, n).round(-2),
        "existing_loans": rng.poisson(1.0, n),
        "age": rng.integers(21, 65, n),
        "years_in_business": rng.integers(0, 25, n),
        "city": rng.choice(["Hyderabad", "Karachi", "Sukkur", "Larkana"], n),
    })
    logit = (-2 + df["monthly_income"] / 25_000 - 0.9 * df["existing_loans"]
             + 0.08 * df["years_in_business"] + (df["city"] == "Karachi") * 0.3)
    df["repaid"] = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    return df


def build(model):
    pre = ColumnTransformer([("num", StandardScaler(), NUM),
                             ("cat", OneHotEncoder(handle_unknown="ignore"), CAT)])
    return make_pipeline(pre, model)


def train_models(df):
    X, y = df[NUM + CAT], df["repaid"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=0)
    models = {"logreg": build(LogisticRegression(max_iter=1000)),
              "knn": build(KNeighborsClassifier(n_neighbors=15))}
    scores = {n: round(m.fit(X_tr, y_tr).score(X_te, y_te), 3) for n, m in models.items()}
    return models, scores


def screen(model, applicant, threshold=0.6):
    p = model.predict_proba(pd.DataFrame([applicant]))[0, 1]
    return round(float(p), 3), "approve" if p >= threshold else "refer to officer"


if __name__ == "__main__":
    df = make_applicants()
    models, scores = train_models(df)
    print("test accuracy:", scores, "| base rate:", round(df["repaid"].mean(), 3))
    strong = {"monthly_income": 150_000, "existing_loans": 0, "age": 40, "years_in_business": 12, "city": "Karachi"}
    weak = {"monthly_income": 20_000, "existing_loans": 4, "age": 25, "years_in_business": 0, "city": "Sukkur"}
    print("strong:", screen(models["logreg"], strong), "| weak:", screen(models["logreg"], weak))
    assert scores["logreg"] > max(df["repaid"].mean(), 1 - df["repaid"].mean())
    assert screen(models["logreg"], strong)[1] == "approve"
    assert screen(models["logreg"], weak)[1] == "refer to officer"
    print("All checks passed")
