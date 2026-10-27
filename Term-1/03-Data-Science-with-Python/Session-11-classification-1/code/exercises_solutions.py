"""Session 11 - Practice exercise solutions."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

if __name__ == "__main__":
    sig = 1 / (1 + np.exp(-2.2))
    assert abs(sig - 0.90) < 0.01

    X, y = make_classification(n_samples=500, n_features=5, n_informative=3, random_state=0)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, random_state=0, stratify=y)
    acc = LogisticRegression().fit(X_tr, y_tr).score(X_te, y_te)
    assert acc > 0.7

    scores = {k: make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k)).fit(X_tr, y_tr).score(X_te, y_te)
              for k in range(1, 31)}
    best_k = max(scores, key=scores.get)
    print("logreg acc", round(acc, 3), "| best k", best_k, round(scores[best_k], 3))

    X_big = X.copy(); X_big[:, 4] = X_big[:, 4] * 10_000 + 50_000
    Xb_tr, Xb_te = train_test_split(X_big, random_state=0, stratify=y)
    raw = KNeighborsClassifier(n_neighbors=best_k).fit(Xb_tr, y_tr).score(Xb_te, y_te)
    scaled = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=best_k)).fit(Xb_tr, y_tr).score(Xb_te, y_te)
    print("unscaled", round(raw, 3), "| scaled", round(scaled, 3))
    assert scaled > raw
    print("All exercise checks passed")
