"""Session 04 - README image: Isolation Forest and LOF on 2-D data."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

X, _ = make_blobs(400, centers=[[0, 0], [5, 5]], cluster_std=[0.8, 1.5], random_state=4)
X = np.vstack([X, np.random.default_rng(4).uniform(-4, 10, (15, 2))])
iso = IsolationForest(contamination=0.04, random_state=0).fit(X)
lof = LocalOutlierFactor(n_neighbors=20, contamination=0.04).fit_predict(X)
gx, gy = np.meshgrid(np.linspace(-5, 11, 200), np.linspace(-5, 11, 200))
s = -iso.score_samples(np.c_[gx.ravel(), gy.ravel()]).reshape(gx.shape)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), layout="constrained")
axes[0].contourf(gx, gy, s, levels=20, cmap="Reds"); axes[0].scatter(X[:, 0], X[:, 1], s=8, c="k")
axes[0].scatter(*X[iso.predict(X) == -1].T, s=60, facecolors="none", edgecolors="blue", label="flagged")
axes[0].set_title("Isolation Forest anomaly score"); axes[0].legend()
axes[1].scatter(X[:, 0], X[:, 1], s=8, c="k")
axes[1].scatter(*X[lof == -1].T, s=60, facecolors="none", edgecolors="green", label="flagged")
axes[1].set_title("Local Outlier Factor flags"); axes[1].legend()
fig.savefig("../images/anomaly.png", dpi=110); plt.close(fig)
print("saved anomaly.png")
