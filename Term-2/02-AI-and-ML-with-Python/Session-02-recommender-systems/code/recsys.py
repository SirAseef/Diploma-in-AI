"""Small recommender toolkit for Session 02 (original code)."""
import numpy as np


def make_ratings(n_users=60, n_items=25, k=3, density=0.3, seed=2):
    rng = np.random.default_rng(seed)
    U = rng.normal(0, 1, (n_users, k)); V = rng.normal(0, 1, (n_items, k))
    raw = U @ V.T + rng.normal(0, 0.3, (n_users, n_items))
    R_true = np.clip(np.round(3 + 1.2 * raw / raw.std()), 1, 5)
    mask = rng.random((n_users, n_items)) < density
    return R_true, np.where(mask, R_true, 0), mask


def split_mask(mask, frac=0.2, seed=0):
    rng = np.random.default_rng(seed)
    test = mask & (rng.random(mask.shape) < frac)
    return mask & ~test, test


def cosine_rows(A):
    norm = np.linalg.norm(A, axis=1, keepdims=True); norm[norm == 0] = 1
    An = A / norm
    return An @ An.T


def user_knn_predict(R, mask, user, item, k=10):
    means = np.array([R[u, mask[u]].mean() if mask[u].any() else 3.0 for u in range(R.shape[0])])
    C = np.where(mask, R - means[:, None], 0)
    sims = cosine_rows(C)[user]
    cand = [u for u in np.argsort(-sims) if u != user and mask[u, item]][:k]
    if not cand or np.abs(sims[cand]).sum() == 0:
        return means[user]
    return means[user] + (sims[cand] @ C[cand, item]) / np.abs(sims[cand]).sum()


def item_knn_predict(R, mask, user, item, k=8):
    means = np.array([R[mask[:, i], i].mean() if mask[:, i].any() else 3.0 for i in range(R.shape[1])])
    C = np.where(mask, R - means[None, :], 0)
    sims = cosine_rows(C.T)[item]
    cand = [j for j in np.argsort(-sims) if j != item and mask[user, j]][:k]
    if not cand or np.abs(sims[cand]).sum() == 0:
        return means[item]
    return means[item] + (sims[cand] @ C[user, cand]) / np.abs(sims[cand]).sum()


def factorise(R, mask, k=3, epochs=400, lr=0.01, reg=2.0, seed=0):
    """Matrix factorisation with user/item biases, trained by full-batch gradient descent.
    Returns P (users x k), Q (items x k) and B, the baseline matrix mu + b_user + b_item."""
    rng = np.random.default_rng(seed)
    n, m = R.shape
    P = rng.normal(0, 0.1, (n, k)); Q = rng.normal(0, 0.1, (m, k))
    bu, bi = np.zeros(n), np.zeros(m)
    mu = R[mask].mean()
    for _ in range(epochs):
        E = np.where(mask, R - (mu + bu[:, None] + bi[None, :] + P @ Q.T), 0)
        bu += lr * (E.sum(1) - reg * bu); bi += lr * (E.sum(0) - reg * bi)
        P, Q = P + lr * (E @ Q - reg * P), Q + lr * (E.T @ P - reg * Q)
    return P, Q, mu + bu[:, None] + bi[None, :]


def rmse(R, R_hat, test_mask):
    return float(np.sqrt(np.mean((R[test_mask] - R_hat[test_mask]) ** 2)))


def top_k(R_hat, seen_mask, user, k=5):
    s = R_hat[user].copy(); s[seen_mask[user]] = -np.inf
    return np.argsort(-s)[:k]


def precision_at_k(R_hat, R_true, seen_mask, k=5, liked=4):
    precs = []
    for u in range(R_hat.shape[0]):
        rec = top_k(R_hat, seen_mask, u, k)
        precs.append(np.mean(R_true[u, rec] >= liked))
    return float(np.mean(precs))
