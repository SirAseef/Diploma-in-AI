"""Session 01 - Real-life problem: rule vs learned model for exam pass prediction."""
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

FEATURES = ["attendance_pct", "assignments_submitted", "quiz_avg"]


def make_students(n=400, seed=7):
    rng = np.random.default_rng(seed)
    att = rng.uniform(40, 100, n).round(0)
    asg = rng.integers(0, 11, n)
    quiz = rng.uniform(0, 20, n).round(1)
    score = 0.03 * att + 0.25 * asg + 0.15 * quiz + rng.normal(0, 0.6, n)
    return pd.DataFrame({"attendance_pct": att, "assignments_submitted": asg, "quiz_avg": quiz,
                         "passed": (score > 6.0).astype(int)})


def rule(df):
    return ((df.attendance_pct >= 75) & (df.quiz_avg >= 10)).astype(int)


def compare(df, seed=0):
    X, y = df[FEATURES], df["passed"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=seed, stratify=y)
    tree = DecisionTreeClassifier(max_depth=3, random_state=seed).fit(X_tr, y_tr)
    return {"rule": accuracy_score(y_te, rule(X_te)), "tree": accuracy_score(y_te, tree.predict(X_te))}


if __name__ == "__main__":
    df = make_students()
    print(df.head()); print("pass rate:", df.passed.mean().round(2))
    res = compare(df)
    print({k: round(v, 3) for k, v in res.items()})
    assert len(df) == 400 and set(df.passed.unique()) == {0, 1}
    assert res["tree"] > res["rule"], "learned model should beat the hand rule"
    print("winner:", max(res, key=res.get))
