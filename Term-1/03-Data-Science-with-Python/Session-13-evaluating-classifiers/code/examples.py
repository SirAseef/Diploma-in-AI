"""Session 13 - Evaluating classifiers: worked examples."""

# %% [markdown]
# ## Example 1 - the accuracy trap

# %%
import numpy as np
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score, roc_curve)
y_true = np.array([0] * 98 + [1] * 2)
always_no = np.zeros(100, dtype=int)
print("accuracy:", accuracy_score(y_true, always_no), "| recall:", recall_score(y_true, always_no))

# %% [markdown]
# ## Example 2 - confusion matrix and report

# %%
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
X, y = make_classification(n_samples=2000, n_features=8, n_informative=5, weights=[0.9], random_state=13)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, stratify=y, random_state=0)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X_tr, y_tr)
pred = model.predict(X_te)
print(confusion_matrix(y_te, pred))
print(classification_report(y_te, pred, digits=3))

# %% [markdown]
# ## Example 3 - metrics by hand

# %%
tn, fp, fn, tp = confusion_matrix(y_te, pred).ravel()
precision, recall = tp / (tp + fp), tp / (tp + fn)
f1 = 2 * precision * recall / (precision + recall)
print(f"precision {precision:.3f} recall {recall:.3f} f1 {f1:.3f}")
assert abs(f1 - f1_score(y_te, pred)) < 1e-12

# %% [markdown]
# ## Example 4 - ROC curve and AUC

# %%
proba = model.predict_proba(X_te)[:, 1]
fpr, tpr, thr = roc_curve(y_te, proba)
print("AUC:", round(roc_auc_score(y_te, proba), 3), "| curve points:", len(thr))

# %% [markdown]
# ## Example 5 - choosing a threshold by cost

# %%
def total_cost(threshold, fn_cost=50_000, fp_cost=2_000):
    p = (proba >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_te, p).ravel()
    return fn * fn_cost + fp * fp_cost

grid = np.round(np.linspace(0.05, 0.95, 19), 2)
best = min(grid, key=total_cost)
print("best threshold:", best, "| cost:", total_cost(best), "vs at 0.5:", total_cost(0.5))
assert total_cost(best) <= total_cost(0.5)

# %% [markdown]
# ## Example 6 - cross-validation and grid search

# %%
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_validate
cv = StratifiedKFold(5, shuffle=True, random_state=0)
scores = cross_validate(model, X, y, cv=cv, scoring=["accuracy", "precision", "recall", "f1", "roc_auc"])
print({k[5:]: round(v.mean(), 3) for k, v in scores.items() if k.startswith("test_")})
grid_search = GridSearchCV(RandomForestClassifier(n_estimators=100, random_state=0),
                           {"max_depth": [3, 6, None], "class_weight": [None, "balanced"]}, scoring="f1", cv=cv)
grid_search.fit(X_tr, y_tr)
print("best params:", grid_search.best_params_, "| CV F1:", round(grid_search.best_score_, 3))
