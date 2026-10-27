"""Session 14 - Introduction to Different Types of Machine Learning: worked examples."""

# %% [markdown]
# ## Example 1 - supervised classification: K-Nearest Neighbours on the Iris flowers

# %%
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris, make_blobs
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, mean_absolute_error

iris = load_iris()
X_tr, X_te, y_tr, y_te = train_test_split(iris.data, iris.target, test_size=0.25, random_state=0, stratify=iris.target)
knn = KNeighborsClassifier(n_neighbors=5).fit(X_tr, y_tr)        # 1. learn
pred = knn.predict(X_te)                                          # 2. predict
print("accuracy:", accuracy_score(y_te, pred))                    # 3. evaluate
print("new flower ->", iris.target_names[knn.predict([[5.9, 3.0, 5.1, 1.8]])[0]])

# %% [markdown]
# ## Example 2 - the same fit/predict pattern with a different model

# %%
tree = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X_tr, y_tr)
print("tree accuracy:", accuracy_score(y_te, tree.predict(X_te)))

# %% [markdown]
# ## Example 3 - supervised regression: predict house price from size

# %%
rng = np.random.default_rng(1)
size = rng.uniform(500, 3000, 80).reshape(-1, 1)            # square feet
price = 0.02 * size.ravel() + 5 + rng.normal(0, 4, 80)       # lakh rupees
reg = LinearRegression().fit(size, price)
print(f"price ≈ {reg.coef_[0]:.4f} × sqft + {reg.intercept_:.2f}")
print("1,200 sq ft ->", round(reg.predict([[1200]])[0], 1), "lakh")
print("MAE:", round(mean_absolute_error(price, reg.predict(size)), 2))

# %% [markdown]
# ## Example 4 - unsupervised clustering: customer segments with K-Means

# %%
customers = pd.DataFrame({
    "visits_per_month": np.r_[rng.normal(2, 0.7, 30), rng.normal(8, 1, 30), rng.normal(15, 2, 30)],
    "avg_spend_k": np.r_[rng.normal(1.5, 0.4, 30), rng.normal(4, 0.8, 30), rng.normal(2, 0.5, 30)],
})
km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(customers)
customers["segment"] = km.labels_
print(customers.groupby("segment").mean().round(1))

# %% [markdown]
# ## Example 5 - unsupervised dimensionality reduction: PCA 4D -> 2D

# %%
pca = PCA(n_components=2).fit(iris.data)
X2 = pca.transform(iris.data)
print(X2[:3].round(2))
print("variance kept:", pca.explained_variance_ratio_.sum().round(3))

# %% [markdown]
# ## Example 6 - reinforcement learning in miniature: an epsilon-greedy bandit
# Three ad banners with hidden click rates. The agent learns which one to show by trial and reward.

# %%
true_click_rate = [0.05, 0.12, 0.08]
estimates, counts = np.zeros(3), np.zeros(3)
eps, total_reward = 0.1, 0
for step in range(5000):
    arm = rng.integers(3) if rng.random() < eps else int(np.argmax(estimates))   # explore vs exploit
    reward = rng.random() < true_click_rate[arm]                                  # environment responds
    counts[arm] += 1
    estimates[arm] += (reward - estimates[arm]) / counts[arm]                     # update from reward
    total_reward += reward
print("estimated rates:", estimates.round(3), "| shown:", counts.astype(int))
print("best banner learned:", int(np.argmax(estimates)), "| clicks:", int(total_reward))
