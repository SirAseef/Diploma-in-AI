"""Session 14 - Clustering: worked examples."""

# %% [markdown]
# ## Data: supermarket customers (synthetic)

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
rng = np.random.default_rng(14)
groups = [(2, 1500, 120), (8, 2500, 120), (4, 7000, 120)]     # (visits, basket Rs, count)
customers = pd.DataFrame(np.vstack([np.column_stack([rng.normal(v, 0.8, n), rng.normal(b, b * 0.12, n)])
                                    for v, b, n in groups]), columns=["visits_per_month", "avg_basket"])
print(customers.describe().round(1))

# %% [markdown]
# ## Example 1 - k-means

# %%
X = StandardScaler().fit_transform(customers[["visits_per_month", "avg_basket"]])
km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
customers["cluster"] = km.labels_
print(customers.groupby("cluster").mean().round(0))

# %% [markdown]
# ## Example 2 - the elbow method

# %%
inertia = {k: round(KMeans(k, n_init=10, random_state=0).fit(X).inertia_, 1) for k in range(1, 9)}
print(inertia)
plt.plot(list(inertia), list(inertia.values()), marker="o"); plt.xlabel("k"); plt.ylabel("inertia"); plt.show()

# %% [markdown]
# ## Example 3 - silhouette score

# %%
sil = {k: round(silhouette_score(X, KMeans(k, n_init=10, random_state=0).fit_predict(X)), 3) for k in range(2, 7)}
print(sil)
assert max(sil, key=sil.get) == 3

# %% [markdown]
# ## Example 4 - why scaling matters

# %%
raw_labels = KMeans(3, n_init=10, random_state=0).fit_predict(customers[["visits_per_month", "avg_basket"]])
print("unscaled clusters, mean visits:", customers.groupby(raw_labels)["visits_per_month"].mean().round(1).tolist())
print("scaled clusters,   mean visits:", customers.groupby("cluster")["visits_per_month"].mean().round(1).tolist())

# %% [markdown]
# ## Example 5 - hierarchical clustering

# %%
from scipy.cluster.hierarchy import dendrogram, linkage
Z = linkage(X[::9], method="ward")
dendrogram(Z, no_labels=True); plt.title("Dendrogram (every 9th customer)"); plt.show()
agg = AgglomerativeClustering(n_clusters=3, linkage="ward").fit_predict(X)
print(pd.crosstab(customers["cluster"], agg))

# %% [markdown]
# ## Example 6 - DBSCAN

# %%
from sklearn.datasets import make_moons
Xm, _ = make_moons(300, noise=0.06, random_state=0)
Xm = np.vstack([Xm, [[2.5, 1.5], [-1.5, -0.8]]])         # two odd points
db = DBSCAN(eps=0.2, min_samples=5).fit(Xm)
print("labels found:", sorted(set(db.labels_)), "| noise points:", int((db.labels_ == -1).sum()))
