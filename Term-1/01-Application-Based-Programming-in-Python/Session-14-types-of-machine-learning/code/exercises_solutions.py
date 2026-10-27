"""Session 14 - practice exercise solutions."""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_wine, make_blobs
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# 1. Classify each scenario as supervised-classification / supervised-regression / unsupervised / reinforcement
SCENARIOS = {
    "predict tomorrow's PSX index value": "supervised-regression",
    "flag an email as spam or not": "supervised-classification",
    "group news articles by topic without labels": "unsupervised",
    "teach a robot to walk by rewarding balance": "reinforcement",
    "estimate a used car's price": "supervised-regression",
    "detect unusual card transactions with no fraud labels": "unsupervised",
}


# 2. KNN on the wine dataset: try k = 1..15 and return the best k (with scaling)
def best_k(seed=0):
    X, y = load_wine(return_X_y=True)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=seed, stratify=y)
    scores = {}
    for k in range(1, 16):
        model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k)).fit(X_tr, y_tr)
        scores[k] = accuracy_score(y_te, model.predict(X_te))
    k = max(scores, key=scores.get)
    return k, scores[k]


# 3. Elbow method: inertia for k = 1..8 on blob data; return the inertias
def elbow(seed=0):
    X, _ = make_blobs(n_samples=300, centers=4, random_state=seed)
    return [KMeans(k, n_init=10, random_state=0).fit(X).inertia_ for k in range(1, 9)]


# 4. Write a 1-nearest-neighbour classifier from scratch
def nn_predict(X_train, y_train, x):
    d = np.sqrt(((np.asarray(X_train) - np.asarray(x)) ** 2).sum(axis=1))
    return y_train[int(np.argmin(d))]


if __name__ == "__main__":
    for s, t in SCENARIOS.items():
        print(f"{t:28s} <- {s}")
    k, acc = best_k(); print("best k:", k, "accuracy:", round(acc, 3)); assert acc > 0.9
    inert = elbow(); print([round(i) for i in inert])
    drops = -np.diff(inert); assert drops[2] > 3 * drops[3]      # elbow at k=4
    Xt = np.array([[1, 1], [1, 2], [8, 8], [9, 8]]); yt = np.array(["A", "A", "B", "B"])
    assert nn_predict(Xt, yt, [2, 1]) == "A" and nn_predict(Xt, yt, [7, 9]) == "B"
    print("all exercise checks passed")
