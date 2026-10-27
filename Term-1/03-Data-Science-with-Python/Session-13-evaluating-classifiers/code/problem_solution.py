"""Session 13 - Real-life problem: cost-aware diabetes screening threshold."""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ["glucose", "bmi", "age", "family_history"]


def make_patients(n=3000, seed=3):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({"glucose": rng.normal(110, 25, n).round(0), "bmi": rng.normal(26, 4.5, n).round(1),
                       "age": rng.integers(20, 75, n), "family_history": rng.integers(0, 2, n)})
    logit = -14 + 0.07 * df["glucose"] + 0.12 * df["bmi"] + 0.03 * df["age"] + 0.9 * df["family_history"]
    df["diabetic"] = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    return df


def cost(y, proba, t, fn_cost=80_000, fp_cost=3_000):
    tn, fp, fn, tp = confusion_matrix(y, (proba >= t).astype(int), labels=[0, 1]).ravel()
    return int(fn * fn_cost + fp * fp_cost)


def lab_screening(df):
    X, y = df[FEATURES], df["diabetic"]
    X_tmp, X_te, y_tmp, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=0)
    X_tr, X_val, y_tr, y_val = train_test_split(X_tmp, y_tmp, test_size=0.25, stratify=y_tmp, random_state=0)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X_tr, y_tr)
    grid = np.round(np.linspace(0.02, 0.9, 45), 2)
    p_val = model.predict_proba(X_val)[:, 1]
    best_t = float(min(grid, key=lambda t: cost(y_val, p_val, t)))
    p_te = model.predict_proba(X_te)[:, 1]
    report = {t: {"recall": round(recall_score(y_te, p_te >= t), 3),
                  "precision": round(precision_score(y_te, p_te >= t), 3),
                  "cost": cost(y_te, p_te, t)} for t in (0.5, best_t)}
    print(confusion_matrix(y_te, (p_te >= 0.5).astype(int)))
    return best_t, report, round(roc_auc_score(y_te, p_te), 3)


if __name__ == "__main__":
    df = make_patients()
    best_t, report, auc = lab_screening(df)
    print("prevalence:", round(df["diabetic"].mean(), 3), "| AUC:", auc, "| best threshold:", best_t)
    for t, r in report.items():
        print(f"threshold {t}: {r}")
    assert best_t < 0.5                                   # misses are costly -> lower threshold
    assert report[best_t]["recall"] > report[0.5]["recall"]
    assert report[best_t]["cost"] < report[0.5]["cost"]
    print("All checks passed")
