"""Session 01 - Machine Learning: worked examples."""

# %% [markdown]
# ## Example 1 - a hand-written rule vs a learned rule

# %%
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris, make_blobs, make_regression
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

rng = np.random.default_rng(1)
hours = rng.uniform(0, 10, 200)
passed = (hours + rng.normal(0, 1, 200) > 4).astype(int)

def rule_based(h):
    return (h >= 5).astype(int)

tree = DecisionTreeClassifier(max_depth=1).fit(hours.reshape(-1, 1), passed)
print("learned cut-off:", round(tree.tree_.threshold[0], 2))
print("rule accuracy :", (rule_based(hours) == passed).mean().round(3))
print("tree accuracy :", round(tree.score(hours.reshape(-1, 1), passed), 3))

# %% [markdown]
# ## Example 2 - supervised classification workflow

# %%
X, y = load_iris(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
model = LogisticRegression(max_iter=500).fit(X_tr, y_tr)
print("test accuracy:", round(model.score(X_te, y_te), 3))
print("first 5 predictions:", model.predict(X_te[:5]), "truth:", y_te[:5])

# %% [markdown]
# ## Example 3 - supervised regression

# %%
Xr, yr = make_regression(n_samples=200, n_features=1, noise=10, random_state=1)
reg = LinearRegression().fit(Xr, yr)
print("slope:", reg.coef_.round(2), "intercept:", round(reg.intercept_, 2), "R^2:", round(reg.score(Xr, yr), 3))

# %% [markdown]
# ## Example 4 - unsupervised clustering

# %%
Xb, _ = make_blobs(n_samples=300, centers=3, random_state=2)
labels = KMeans(n_clusters=3, n_init=10, random_state=0).fit_predict(Xb)
print("cluster sizes:", np.bincount(labels))

# %% [markdown]
# ## Example 5 - spotting overfitting

# %%
for depth in [1, 3, None]:
    t = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(X_tr, y_tr)
    print(f"depth={depth}: train={t.score(X_tr, y_tr):.3f} test={t.score(X_te, y_te):.3f}")

# %% [markdown]
# ## Example 6 - a reinforcement-learning flavour: epsilon-greedy bandit

# %%
true_means = np.array([1.0, 2.5, 1.8])
estimates, counts = np.zeros(3), np.zeros(3)
for step in range(500):
    arm = rng.integers(3) if rng.random() < 0.1 else int(estimates.argmax())
    reward = rng.normal(true_means[arm], 1)
    counts[arm] += 1
    estimates[arm] += (reward - estimates[arm]) / counts[arm]
print("estimates:", estimates.round(2), "pulls:", counts.astype(int))
print("best arm found:", int(estimates.argmax()))
