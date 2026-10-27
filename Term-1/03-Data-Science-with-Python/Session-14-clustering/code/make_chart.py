"""Session 14 - README image: k-means, elbow, DBSCAN vs k-means on moons."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import make_blobs, make_moons
from sklearn.preprocessing import StandardScaler

X, _ = make_blobs(500, centers=4, cluster_std=1.0, random_state=14)
X = StandardScaler().fit_transform(X)
km = KMeans(4, n_init=10, random_state=0).fit(X)
inertia = [KMeans(k, n_init=10, random_state=0).fit(X).inertia_ for k in range(1, 10)]
Xm, _ = make_moons(400, noise=0.06, random_state=0)
fig, axes = plt.subplots(1, 4, figsize=(16, 3.8), layout="constrained")
axes[0].scatter(X[:, 0], X[:, 1], c=km.labels_, s=10, cmap="tab10")
axes[0].scatter(*km.cluster_centers_.T, c="black", marker="X", s=120)
axes[0].set_title("k-means (k = 4)")
axes[1].plot(range(1, 10), inertia, marker="o"); axes[1].axvline(4, ls="--", color="grey")
axes[1].set(title="Elbow method", xlabel="k", ylabel="inertia")
axes[2].scatter(Xm[:, 0], Xm[:, 1], c=KMeans(2, n_init=10, random_state=0).fit_predict(Xm), s=10, cmap="coolwarm")
axes[2].set_title("k-means on moons (wrong split)")
axes[3].scatter(Xm[:, 0], Xm[:, 1], c=DBSCAN(eps=0.2, min_samples=5).fit_predict(Xm), s=10, cmap="coolwarm")
axes[3].set_title("DBSCAN on moons (correct)")
fig.savefig("../images/clustering.png", dpi=105)
plt.close(fig)
print("chart written")
