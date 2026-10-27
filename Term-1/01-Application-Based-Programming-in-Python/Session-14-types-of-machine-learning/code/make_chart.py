"""Generate README illustrations for Session 14 (saved to ../images/)."""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

X, y = make_blobs(n_samples=150, centers=3, cluster_std=1.1, random_state=4)
fig, axs = plt.subplots(1, 3, figsize=(13, 4))
for k, m in zip(range(3), ["o", "s", "^"]):
    axs[0].scatter(*X[y == k].T, marker=m, label=f"class {k}")
axs[0].set_title("Supervised: data comes WITH labels"); axs[0].legend()
axs[1].scatter(*X.T, color="grey"); axs[1].set_title("Unsupervised: same data, NO labels")
km = KMeans(3, n_init=10, random_state=0).fit(X)
axs[2].scatter(*X.T, c=km.labels_, cmap="viridis")
axs[2].scatter(*km.cluster_centers_.T, color="red", marker="X", s=200, label="centres")
axs[2].set_title("K-Means discovers the groups itself"); axs[2].legend()
fig.tight_layout(); fig.savefig("../images/supervised_vs_unsupervised.png", dpi=100); plt.close(fig)

# regression vs classification
rng = np.random.default_rng(0)
fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
x = rng.uniform(500, 3000, 40); p = 0.02 * x + rng.normal(0, 6, 40)
axs[0].scatter(x, p); xs = np.linspace(500, 3000, 2); axs[0].plot(xs, 0.02 * xs, "r-")
axs[0].set_title("Regression → predict a NUMBER\n(house size → price in lakh)"); axs[0].set_xlabel("sq ft")
h = rng.uniform(0, 10, 60); passed = (h + rng.normal(0, 1.5, 60) > 5).astype(int)
axs[1].scatter(h, passed, c=passed, cmap="coolwarm"); axs[1].axvline(5, ls="--", color="k")
axs[1].set_yticks([0, 1], ["fail", "pass"]); axs[1].set_xlabel("study hours")
axs[1].set_title("Classification → predict a CATEGORY\n(study hours → pass / fail)")
fig.tight_layout(); fig.savefig("../images/regression_vs_classification.png", dpi=100); plt.close(fig)
print("images written")
