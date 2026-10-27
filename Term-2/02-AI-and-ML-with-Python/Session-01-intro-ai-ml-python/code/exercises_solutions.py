"""Session 01 - Practice exercise solutions."""
# notebook: run-in-code-dir
import os
import joblib
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from examples import CAT, NUM, make_students, pre


def ex1():
    X, y = load_breast_cancer(return_X_y=True)
    return cross_val_score(make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)), X, y, cv=5).mean()


def ex2(seed=0):
    rng = np.random.default_rng(seed)
    X, y = load_breast_cancer(return_X_y=True)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    scaled_first = cross_val_score(LogisticRegression(max_iter=1000), StandardScaler().fit_transform(X), y, cv=5).mean()
    proper = cross_val_score(model, X, y, cv=5).mean()
    leaky = np.column_stack([X, y + rng.normal(0, 0.01, len(y))])   # target leakage
    target_leak = cross_val_score(model, leaky, y, cv=5).mean()
    return scaled_first, proper, target_leak


def ex3():
    df = make_students()
    return cross_val_score(Pipeline([("pre", pre), ("m", KNeighborsClassifier(7))]), df[NUM + CAT], df.passed, cv=5).mean()


def ex4():
    X, y = load_breast_cancer(return_X_y=True)
    pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X, y)
    os.makedirs("output", exist_ok=True); p = "output/bc.joblib"
    joblib.dump(pipe, p)
    return bool((joblib.load(p).predict(X) == pipe.predict(X)).all())


if __name__ == "__main__":
    a = ex1(); print("ex1", round(a, 3)); assert a > 0.95
    s, p, t = ex2(); print("ex2 scaled-first", round(s, 3), "pipeline", round(p, 3), "target leak", round(t, 3))
    assert abs(s - p) < 0.02 and t > 0.99
    k = ex3(); print("ex3 knn", round(k, 3)); assert k > 0.6
    assert ex4(); print("ex4 identical predictions")
    print("all exercises OK")
