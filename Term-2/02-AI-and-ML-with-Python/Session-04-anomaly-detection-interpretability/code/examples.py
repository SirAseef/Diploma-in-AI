"""Session 04 - Anomaly Detection and Model Interpretability: worked examples."""

# %% [markdown]
# ## Example 1 - z-score and IQR on one feature

# %%
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.inspection import partial_dependence, permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(4)
amount = np.concatenate([rng.lognormal(7.5, 0.5, 990), rng.uniform(40000, 150000, 10)])
z = (amount - amount.mean()) / amount.std()
q1, q3 = np.percentile(amount, [25, 75]); iqr = q3 - q1
print("z-score flags:", int((np.abs(z) > 3).sum()), "| IQR flags:", int(((amount < q1 - 1.5 * iqr) | (amount > q3 + 1.5 * iqr)).sum()))

# %% [markdown]
# ## Example 2 - Isolation Forest on several features

# %%
n = 1000
X = np.column_stack([rng.lognormal(7.5, 0.5, n), rng.normal(14, 3, n), rng.exponential(5, n)])
y = np.zeros(n, int)
idx = rng.choice(n, 20, replace=False); y[idx] = 1
X[idx] = np.column_stack([rng.uniform(30000, 90000, 20), rng.uniform(0, 5, 20), rng.uniform(40, 200, 20)])
Xs = StandardScaler().fit_transform(np.log1p(X))
iso = IsolationForest(contamination=0.02, random_state=0).fit(Xs)
scores = -iso.score_samples(Xs)
print("flagged:", int((iso.predict(Xs) == -1).sum()))

# %% [markdown]
# ## Example 3 - Local Outlier Factor

# %%
lof_flags = LocalOutlierFactor(n_neighbors=20, contamination=0.02).fit_predict(Xs) == -1
print("LOF flagged:", int(lof_flags.sum()), "true anomalies among them:", int(y[lof_flags].sum()))

# %% [markdown]
# ## Example 4 - evaluating with precision@k and PR-AUC

# %%
def precision_at_k(y, scores, k):
    return y[np.argsort(-scores)[:k]].mean()

print("precision@20:", precision_at_k(y, scores, 20), "PR-AUC:", round(average_precision_score(y, scores), 3))

# %% [markdown]
# ## Example 5 - permutation importance

# %%
data = load_breast_cancer()
X_tr, X_te, y_tr, y_te = train_test_split(data.data, data.target, random_state=0, stratify=data.target)
clf = RandomForestClassifier(200, random_state=0).fit(X_tr, y_tr)
r = permutation_importance(clf, X_te, y_te, n_repeats=10, random_state=0)
for i in np.argsort(-r.importances_mean)[:5]:
    print(f"{data.feature_names[i]:25s} {r.importances_mean[i]:.4f}")

# %% [markdown]
# ## Example 6 - partial dependence and a local explanation

# %%
top = int(np.argsort(-r.importances_mean)[0])
pdep = partial_dependence(clf, X_te, features=[top], grid_resolution=10)
print("partial dependence of", data.feature_names[top], ":", pdep["average"][0].round(2))
sc = StandardScaler().fit(X_tr)
lr = LogisticRegression(max_iter=2000).fit(sc.transform(X_tr), y_tr)
x = sc.transform(X_te[:1])[0]
contrib = lr.coef_[0] * x
for i in np.argsort(contrib)[:3]:
    print(f"pushes towards malignant: {data.feature_names[i]:25s} {contrib[i]:.2f}")
