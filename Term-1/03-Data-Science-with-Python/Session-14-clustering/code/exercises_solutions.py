"""Session 14 - Practice exercise solutions."""
import numpy as np
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.datasets import make_blobs, make_circles, make_moons
from sklearn.metrics import adjusted_rand_score

if __name__ == "__main__":
    X, y, centres = make_blobs(600, centers=4, random_state=1, return_centers=True)
    km = KMeans(4, n_init=10, random_state=0).fit(X)
    # each true centre should have a found centre close to it
    dists = [np.min(np.linalg.norm(km.cluster_centers_ - c, axis=1)) for c in centres]
    assert max(dists) < 0.5

    inertia = [KMeans(k, n_init=10, random_state=0).fit(X).inertia_ for k in range(1, 11)]
    drops = -np.diff(inertia)
    elbow = int(np.argmax(drops[:-1] / drops[1:])) + 2      # biggest change in the rate of improvement
    print("elbow at k =", elbow)
    assert elbow == 4

    Xc, yc = make_circles(500, factor=0.4, noise=0.04, random_state=0)
    ari_db = adjusted_rand_score(yc, DBSCAN(eps=0.2).fit_predict(Xc))
    ari_km = adjusted_rand_score(yc, KMeans(2, n_init=10, random_state=0).fit_predict(Xc))
    print("circles ARI: DBSCAN", round(ari_db, 3), "| k-means", round(ari_km, 3))
    assert ari_db > 0.9 > ari_km

    Xm, ym = make_moons(300, noise=0.05, random_state=0)
    ari = {link: adjusted_rand_score(ym, AgglomerativeClustering(2, linkage=link).fit_predict(Xm)) for link in ("single", "ward")}
    print("moons ARI:", {k: round(v, 3) for k, v in ari.items()})
    assert ari["single"] > ari["ward"]
    print("All exercise checks passed")
