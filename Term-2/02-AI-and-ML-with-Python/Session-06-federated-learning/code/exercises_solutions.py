"""Session 06 - Practice exercise solutions."""
# notebook: run-in-code-dir
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from fl import accuracy, fedavg, local_train, split_clients

X, y = make_classification(3000, n_features=10, n_informative=6, random_state=6)
X = StandardScaler().fit_transform(X)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, random_state=0)
non_iid = split_clients(X_tr, y_tr, 5, iid=False)


def ex1():
    iid = fedavg(split_clients(X_tr, y_tr, 5, iid=True), rounds=10, X_test=X_te, y_test=y_te)[1][-1]
    nid = fedavg(non_iid, rounds=10, X_test=X_te, y_test=y_te)[1][-1]
    return iid, nid


def ex2():
    return {e: fedavg(non_iid, rounds=10, epochs=e, X_test=X_te, y_test=y_te)[1][-1] for e in (1, 5, 20)}


def ex3():
    bad = list(non_iid)
    Xb, yb = bad[0]
    bad[0] = (Xb, 1 - yb)                      # a malicious client with flipped labels...
    def poisoned(agg):
        w = np.zeros(X.shape[1] + 1)
        for r in range(10):
            ups = [local_train(w, Xk, yk, 5, seed=r) - w for Xk, yk in bad]
            ups[0] = 100 * ups[0]               # ...that also scales its update by 100
            U = np.stack(ups)
            w = w + (np.median(U, axis=0) if agg == "median" else U.mean(0))
        return accuracy(w, X_te, y_te)
    return poisoned("mean"), poisoned("median")


def ex4():
    return {s: fedavg(non_iid, rounds=20, X_test=X_te, y_test=y_te, dp_clip=1.0, dp_sigma=s, seed=3)[1][-1]
            for s in (0, 0.5, 1, 2)}


if __name__ == "__main__":
    a, b = ex1(); print("ex1 IID", round(a, 3), "non-IID", round(b, 3)); assert a > 0.7 and b > 0.6
    e = ex2(); print("ex2", {k: round(v, 3) for k, v in e.items()})
    m, med = ex3(); print("ex3 poisoned mean", round(m, 3), "median", round(med, 3)); assert med > m
    d = ex4(); print("ex4", {k: round(v, 3) for k, v in d.items()}); assert d[0] >= d[2] - 0.02
    print("all exercises OK")
