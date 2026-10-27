"""Session 02 - Real-life problem: hybrid drama recommender with cold start."""
# notebook: run-in-code-dir
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from recsys import factorise, rmse, split_mask

GENRES = ["romance", "family", "thriller", "comedy", "historical"]


def make_app(n_users=80, n_items=30, seed=8):
    rng = np.random.default_rng(seed)
    item_feats = (rng.random((n_items, len(GENRES))) < 0.35).astype(float)
    item_feats[item_feats.sum(1) == 0, 1] = 1.0           # every drama has at least one genre
    taste = rng.normal(0, 1, (n_users, len(GENRES)))
    raw = taste @ item_feats.T + rng.normal(0, 0.4, (n_users, n_items))
    R_true = np.clip(np.round(3 + 1.3 * (raw - raw.mean()) / raw.std()), 1, 5)
    mask = rng.random((n_users, n_items)) < 0.3
    return item_feats, R_true, np.where(mask, R_true, 0), mask


def hybrid_scores(user, R_hat, item_feats, R, mask, alpha=0.7):
    liked = np.where(mask[user] & (R[user] >= 4))[0]
    profile = item_feats[liked].mean(0) if len(liked) else item_feats.mean(0)
    content = cosine_similarity(profile[None], item_feats)[0] * 5
    scores = alpha * R_hat[user] + (1 - alpha) * content
    scores[mask[user]] = -np.inf
    return scores


def cold_start(item_feats, R, mask, liked_genres):
    profile = np.array([g in liked_genres for g in GENRES], float)
    content = cosine_similarity(profile[None], item_feats)[0]
    pop = np.nan_to_num(np.nanmean(np.where(mask, R, np.nan), axis=0), nan=3) / 5
    return np.argsort(-(0.6 * content + 0.4 * pop))[:5]


if __name__ == "__main__":
    feats, R_true, R, mask = make_app()
    train, test = split_mask(mask)
    R_tr = np.where(train, R, 0)
    P, Q, B = factorise(R_tr, train, k=3)
    mu = R_tr[train].mean()
    R_hat = B + P @ Q.T
    e_mf, e_mean = rmse(R, R_hat, test), rmse(R, np.full(R.shape, mu), test)
    print("RMSE MF:", round(e_mf, 3), "| global mean:", round(e_mean, 3))
    top = np.argsort(-hybrid_scores(0, R_hat, feats, R_tr, train))[:5]
    print("user 0 top-5 hybrid:", top, "true ratings:", R_true[0, top])
    new = cold_start(feats, R_tr, train, {"thriller", "historical"})
    print("new user (thriller/historical) top-5:", new, [", ".join(g for g, f in zip(GENRES, feats[i]) if f) for i in new])
    assert e_mf < e_mean
    assert not train[0, top].any()
    assert sum(feats[i][GENRES.index("thriller")] or feats[i][GENRES.index("historical")] for i in new) >= 3
    print("OK")
