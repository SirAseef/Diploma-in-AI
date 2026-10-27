"""Session 05 - README image: k-means segments in PCA space and silhouette by k."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from shop_data import feature_matrix, make_transactions, rfm_table

X = feature_matrix(rfm_table(make_transactions()))
sil = {k: silhouette_score(X, KMeans(k, n_init=10, random_state=0).fit_predict(X)) for k in range(2, 8)}
best = max(sil, key=sil.get)
labels = KMeans(best, n_init=10, random_state=0).fit_predict(X)
Z = PCA(2, random_state=0).fit_transform(X)
fig, axes = plt.subplots(1, 2, figsize=(11, 4), layout="constrained")
axes[0].scatter(Z[:, 0], Z[:, 1], c=labels, cmap="tab10", s=10); axes[0].set_title(f"k-means segments (k={best}) in PCA space")
axes[1].plot(list(sil), list(sil.values()), marker="o"); axes[1].set(title="Silhouette by k", xlabel="k", ylabel="silhouette")
fig.savefig("../images/segments.png", dpi=110); plt.close(fig)
print("saved segments.png")
