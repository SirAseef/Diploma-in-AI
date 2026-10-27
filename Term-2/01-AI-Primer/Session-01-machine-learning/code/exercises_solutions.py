"""Session 01 - Practice exercise solutions."""
import numpy as np
from sklearn.datasets import load_wine, make_classification
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


def ex1():
    X, y = load_wine(return_X_y=True)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
    return KNeighborsClassifier(5).fit(X_tr, y_tr).score(X_te, y_te)


def ex2():
    return {"news topics": "unsupervised", "electricity bill": "supervised", "ludo bot": "reinforcement"}


def ex3(seed=0):
    rng = np.random.default_rng(seed)
    x = rng.uniform(0, 10, 100)
    y = 3 * x + 2 + rng.normal(0, 0.5, 100)
    return LinearRegression().fit(x.reshape(-1, 1), y).coef_[0]


def ex4():
    X, y = make_classification(800, n_features=12, n_informative=4, flip_y=0.1, random_state=0)
    Xa, Xb, ya, yb = train_test_split(X, y, random_state=0)
    scores = {d: DecisionTreeClassifier(max_depth=d, random_state=0).fit(Xa, ya).score(Xb, yb) for d in range(1, 13)}
    return max(scores, key=scores.get), scores


if __name__ == "__main__":
    a = ex1(); print("ex1 KNN wine accuracy:", round(a, 3)); assert a > 0.6
    k = ex2(); print("ex2", k); assert k["ludo bot"] == "reinforcement"
    s = ex3(); print("ex3 slope:", round(s, 3)); assert abs(s - 3) < 0.1
    best, scores = ex4(); print("ex4 best depth:", best, round(scores[best], 3))
    assert scores[best] >= scores[12]
    print("all exercises OK")
