"""Federated-learning simulator with NumPy logistic regression (original code, Session 06)."""
import numpy as np


def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -30, 30)))


def add_bias(X):
    return np.hstack([X, np.ones((len(X), 1))])


def local_train(w, X, y, epochs=5, lr=0.1, batch=32, seed=0):
    rng = np.random.default_rng(seed)
    w = w.copy(); Xb = add_bias(X)
    for _ in range(epochs):
        idx = rng.permutation(len(X))
        for s in range(0, len(X), batch):
            b = idx[s:s + batch]
            grad = Xb[b].T @ (sigmoid(Xb[b] @ w) - y[b]) / len(b)
            w -= lr * grad
    return w


def accuracy(w, X, y):
    return float(((sigmoid(add_bias(X) @ w) > 0.5) == y).mean())


def split_clients(X, y, n_clients=5, iid=True, seed=0, sizes=None):
    rng = np.random.default_rng(seed)
    if iid:
        idx = rng.permutation(len(X))
        parts = np.array_split(idx, n_clients) if sizes is None else np.split(idx, np.cumsum(sizes)[:-1])
    else:  # sort by first feature so each client sees a different region of the data
        idx = np.argsort(X[:, 0] + rng.normal(0, 0.5, len(X)))
        parts = np.array_split(idx, n_clients) if sizes is None else np.split(idx, np.cumsum(sizes)[:-1])
    return [(X[p], y[p]) for p in parts]


def fedavg(clients, rounds=20, epochs=5, lr=0.1, X_test=None, y_test=None,
           dp_clip=None, dp_sigma=0.0, aggregate="mean", seed=0):
    rng = np.random.default_rng(seed)
    d = clients[0][0].shape[1] + 1
    w = np.zeros(d); history = []
    n_total = sum(len(yk) for _, yk in clients)
    for r in range(rounds):
        updates, weights = [], []
        for k, (Xk, yk) in enumerate(clients):
            delta = local_train(w, Xk, yk, epochs, lr, seed=r * 100 + k) - w
            if dp_clip is not None:
                norm = np.linalg.norm(delta)
                delta = delta * min(1.0, dp_clip / (norm + 1e-12))
                delta = delta + rng.normal(0, dp_sigma * dp_clip, d)
            updates.append(delta); weights.append(len(yk) / n_total)
        U = np.stack(updates)
        w = w + (np.median(U, axis=0) if aggregate == "median" else np.average(U, axis=0, weights=weights))
        if X_test is not None:
            history.append(accuracy(w, X_test, y_test))
    return w, history


def secure_sum(vectors, seed=0):
    """Pairwise additive masking: each pair (i, j) shares a random mask that i adds and j subtracts."""
    rng = np.random.default_rng(seed)
    n = len(vectors)
    masked = [v.astype(float).copy() for v in vectors]
    for i in range(n):
        for j in range(i + 1, n):
            m = rng.normal(0, 100, vectors[0].shape)
            masked[i] += m; masked[j] -= m
    return masked, np.sum(masked, axis=0)
