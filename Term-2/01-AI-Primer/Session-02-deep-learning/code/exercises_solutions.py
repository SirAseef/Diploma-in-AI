"""Session 02 - Practice exercise solutions."""
import warnings
import numpy as np
from sklearn.datasets import load_digits, make_moons
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
warnings.filterwarnings("ignore", category=ConvergenceWarning)


def relu(z):
    return np.maximum(0, z)


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def ex2(w=5.0, lr=0.1, steps=100):
    for _ in range(steps):
        w -= lr * 2 * (w + 1)
    return w


def ex3():
    X, y = make_moons(500, noise=0.2, random_state=0)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, random_state=0)
    mlp = MLPClassifier((16, 16), max_iter=2000, random_state=0).fit(X_tr, y_tr).score(X_te, y_te)
    log = LogisticRegression().fit(X_tr, y_tr).score(X_te, y_te)
    return mlp, log


def ex4():
    X, y = load_digits(return_X_y=True)
    return [c.shape for c in MLPClassifier((32,), max_iter=300, random_state=0).fit(X / 16, y).coefs_]


if __name__ == "__main__":
    z = np.array([-2, 0, 2])
    print("ex1 relu:", relu(z), "sigmoid:", sigmoid(z).round(3))
    assert list(relu(z)) == [0, 0, 2] and abs(sigmoid(0) - 0.5) < 1e-9
    w = ex2(); print("ex2 minimum at:", round(w, 4)); assert abs(w + 1) < 1e-3
    mlp, log = ex3(); print("ex3 mlp:", round(mlp, 3), "logistic:", round(log, 3)); assert mlp > log
    s = ex4(); print("ex4 shapes:", s); assert s == [(64, 32), (32, 10)]
    print("all exercises OK")
