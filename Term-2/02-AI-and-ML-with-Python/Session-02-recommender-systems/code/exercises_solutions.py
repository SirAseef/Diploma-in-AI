"""Session 02 - Practice exercise solutions."""
# notebook: run-in-code-dir
import numpy as np
from sklearn.decomposition import TruncatedSVD
from recsys import factorise, item_knn_predict, make_ratings, rmse, split_mask, top_k, user_knn_predict

R_true, R, mask = make_ratings()
train, test = split_mask(mask)
R_train = np.where(train, R, 0)


def rmse_of(predict):
    pairs = np.argwhere(test)
    pred = np.array([predict(R_train, train, u, i) for u, i in pairs])
    return float(np.sqrt(np.mean((R[test] - pred) ** 2)))


def ex1():
    u, i = np.argwhere(test)[0]
    return item_knn_predict(R_train, train, u, i), R[u, i]


def ex2():
    P, Q, B = factorise(R_train, train, epochs=300)
    return {"user": rmse_of(user_knn_predict), "item": rmse_of(item_knn_predict), "mf": rmse(R, B + P @ Q.T, test)}


def ex3():
    means = np.array([R_train[u, train[u]].mean() if train[u].any() else 3 for u in range(R.shape[0])])
    filled = np.where(train, R_train, means[:, None])
    svd = TruncatedSVD(3, random_state=0).fit(filled)
    return rmse(R, svd.inverse_transform(svd.transform(filled)), test)


def ex4():
    P, Q, B = factorise(R_train, train, epochs=300); R_hat = B + P @ Q.T
    recs = np.concatenate([top_k(R_hat, train, u, 5) for u in range(R.shape[0])])
    return len(set(recs.tolist())) / R.shape[1]


if __name__ == "__main__":
    p, a = ex1(); print("ex1 item-kNN prediction", round(p, 2), "actual", a); assert 1 <= p <= 5.5
    s = ex2(); print("ex2", {k: round(v, 3) for k, v in s.items()}); assert all(v < 1.5 for v in s.values())
    r = ex3(); print("ex3 TruncatedSVD RMSE", round(r, 3)); assert r < 1.5
    c = ex4(); print("ex4 coverage", round(c, 2)); assert 0 < c <= 1
    print("all exercises OK")
