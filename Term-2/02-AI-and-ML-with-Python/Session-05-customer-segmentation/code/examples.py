"""Session 05 - Clustering Techniques for Customer Segmentation: worked examples."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - simulate a transactions log

# %%
import numpy as np
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.mixture import GaussianMixture
from shop_data import feature_matrix, make_transactions, rfm_table

tx = make_transactions(n_customers=600, seed=5)
print(tx.head()); print("rows:", len(tx))

# %% [markdown]
# ## Example 2 - build RFM features

# %%
rfm = rfm_table(tx)
print(rfm.describe().round(1))

# %% [markdown]
# ## Example 3 - k-means with silhouette-based k

# %%
X = feature_matrix(rfm)
sil = {k: round(float(silhouette_score(X, KMeans(k, n_init=10, random_state=0).fit_predict(X))), 3) for k in range(2, 8)}
best_k = max(sil, key=sil.get)
print("silhouette:", sil, "best k:", best_k)
km_labels = KMeans(best_k, n_init=10, random_state=0).fit_predict(X)

# %% [markdown]
# ## Example 4 - Gaussian Mixture: BIC and soft membership

# %%
bic = {k: round(float(GaussianMixture(k, random_state=0).fit(X).bic(X))) for k in range(2, 8)}
print("BIC:", bic, "lowest at k =", min(bic, key=bic.get))
gmm = GaussianMixture(best_k, random_state=0).fit(X)
proba = gmm.predict_proba(X)
print("first 3 customers' membership:", proba[:3].round(2))

# %% [markdown]
# ## Example 5 - agreement between methods and stability

# %%
agg_labels = AgglomerativeClustering(best_k, linkage="ward").fit_predict(X)
km_seed1 = KMeans(best_k, n_init=10, random_state=1).fit_predict(X)
print("k-means vs agglomerative ARI:", round(adjusted_rand_score(km_labels, agg_labels), 3))
print("k-means seed 0 vs seed 1 ARI:", round(adjusted_rand_score(km_labels, km_seed1), 3))
print("k-means vs hidden persona ARI:", round(adjusted_rand_score(rfm.persona, km_labels), 3))

# %% [markdown]
# ## Example 6 - profile segments

# %%
rfm["segment"] = km_labels
profile = rfm.groupby("segment")[["R", "F", "M", "disc"]].median()
profile["size"] = rfm.segment.value_counts().sort_index()
print(profile.round(2))
