"""Session 04 - Practice exercise solutions."""
import numpy as np
from sklearn.datasets import load_breast_cancer, make_blobs
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM


def ex1():
    X, _ = make_blobs(500, centers=3, cluster_std=1.0, random_state=1)
    out = np.random.default_rng(1).uniform(-25, 25, (10, 2))
    Xo = StandardScaler().fit_transform(np.vstack([X, out]))
    dets = {"iforest": IsolationForest(contamination=0.02, random_state=0),
            "lof": LocalOutlierFactor(n_neighbors=20, contamination=0.02),
            "ocsvm": OneClassSVM(nu=0.02, gamma="scale")}
    return {k: int((d.fit_predict(Xo)[-10:] == -1).sum()) for k, d in dets.items()}


def ex2():
    X, _ = make_blobs(1000, centers=2, random_state=0)
    return {c: int((IsolationForest(contamination=c, random_state=0).fit_predict(X) == -1).sum()) for c in (0.01, 0.05, 0.1)}


def ex3():
    d = load_breast_cancer()
    X_tr, X_te, y_tr, y_te = train_test_split(d.data, d.target, random_state=0)
    rf = RandomForestClassifier(200, random_state=0).fit(X_tr, y_tr)
    imp = permutation_importance(rf, X_te, y_te, n_repeats=10, random_state=0).importances_mean
    return [d.feature_names[i] for i in np.argsort(-imp)[:5]]


def ex4():
    d = load_breast_cancer()
    X_tr, X_te, y_tr, y_te = train_test_split(d.data, d.target, random_state=0)
    sc = StandardScaler().fit(X_tr)
    lr = LogisticRegression(max_iter=2000).fit(sc.transform(X_tr), y_tr)
    contrib = lr.coef_[0] * sc.transform(X_te[:1])[0]
    return [d.feature_names[i] for i in np.argsort(contrib)[:3]]


if __name__ == "__main__":
    c = ex1(); print("ex1 caught of 10:", c); assert c["iforest"] >= 8
    f = ex2(); print("ex2 flags:", f); assert f[0.01] < f[0.05] < f[0.1]
    print("ex3 top-5:", ex3()); assert len(ex3()) == 5
    print("ex4 pushes to malignant:", ex4()); assert len(ex4()) == 3
    print("all exercises OK")
