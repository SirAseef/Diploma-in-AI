"""Session 05 - Practice exercise solutions."""
# notebook: run-in-code-dir
import numpy as np
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from shop_data import feature_matrix, make_transactions, rfm_table

rfm = rfm_table(make_transactions())
X = feature_matrix(rfm)


def best_k(X):
    sil = {k: silhouette_score(X, KMeans(k, n_init=10, random_state=0).fit_predict(X)) for k in range(2, 8)}
    return max(sil, key=sil.get)


def ex1():
    extra = StandardScaler().fit_transform(np.log1p((rfm.M / rfm.F).to_numpy())[:, None])
    return best_k(X), best_k(np.hstack([X, extra]))


def ex2(k=4):
    p = GaussianMixture(k, random_state=0).fit(X).predict_proba(X)
    return int((p.max(1) < 0.6).sum())


def ex3(k=4):
    km = KMeans(k, n_init=10, random_state=0).fit_predict(X)
    return {l: adjusted_rand_score(km, AgglomerativeClustering(k, linkage=l).fit_predict(X)) for l in ("ward", "average")}


def ex4():
    return float(PCA(2).fit(X).explained_variance_ratio_.sum())


if __name__ == "__main__":
    a, b = ex1(); print("ex1 best k without/with avg_basket:", a, b); assert 2 <= b <= 7
    u = ex2(); print("ex2 in-between customers:", u); assert u >= 0
    r = ex3(); print("ex3 ARI:", {k: round(v, 3) for k, v in r.items()}); assert r["ward"] > 0.3
    e = ex4(); print("ex4 variance explained by 2 PCs:", round(e, 3)); assert 0.5 < e <= 1
    print("all exercises OK")
