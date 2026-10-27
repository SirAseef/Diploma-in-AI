"""Session 12 - Real-life problem: telecom churn - compare four classifiers."""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, export_text

FEATURES = ["tenure_months", "monthly_spend", "data_gb", "complaints", "dropped_calls", "has_family_bundle"]


def make_customers(n=2000, seed=7):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "tenure_months": rng.integers(1, 96, n),
        "monthly_spend": rng.gamma(3, 300, n).round(0),
        "data_gb": rng.gamma(2, 6, n).round(1),
        "complaints": rng.poisson(0.7, n),
        "dropped_calls": rng.poisson(3, n),
        "has_family_bundle": rng.integers(0, 2, n),
    })
    logit = (0.4 - 0.04 * df["tenure_months"] + 0.9 * df["complaints"] + 0.25 * df["dropped_calls"]
             - 1.2 * df["has_family_bundle"] - 0.0005 * df["monthly_spend"])
    df["churn"] = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    return df


def churn_study(df):
    X, y = df[FEATURES], df["churn"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=0)
    models = {
        "tree": DecisionTreeClassifier(max_depth=4, random_state=0),
        "forest": RandomForestClassifier(n_estimators=300, min_samples_leaf=3, random_state=0),
        "naive_bayes": GaussianNB(),
        "svm": make_pipeline(StandardScaler(), SVC(kernel="rbf", C=1.0)),
    }
    cv = {n: round(cross_val_score(m, X_tr, y_tr, cv=5).mean(), 3) for n, m in models.items()}
    best = max(cv, key=cv.get)
    test_acc = models[best].fit(X_tr, y_tr).score(X_te, y_te)
    forest = models["forest"].fit(X_tr, y_tr)
    drivers = pd.Series(forest.feature_importances_, index=FEATURES).nlargest(3)
    rules = export_text(DecisionTreeClassifier(max_depth=2, random_state=0).fit(X_tr, y_tr), feature_names=FEATURES)
    return cv, best, round(test_acc, 3), drivers, rules


if __name__ == "__main__":
    df = make_customers()
    cv, best, acc, drivers, rules = churn_study(df)
    print("CV accuracy:", cv)
    print("best:", best, "| test accuracy:", acc, "| churn rate:", round(df["churn"].mean(), 3))
    print("top drivers:\n", drivers.round(3))
    print(rules)
    assert acc > max(df["churn"].mean(), 1 - df["churn"].mean())
    assert drivers.index[0] == "tenure_months"   # strongest real driver in the simulation
    print("All checks passed")
