"""Session 12 - Classification II (trees, forests, Naive Bayes, SVM): worked examples."""

# %% [markdown]
# ## Example 1 - Gini impurity by hand

# %%
import numpy as np
import pandas as pd

def gini(counts):
    p = np.array(counts) / sum(counts)
    return 1 - (p ** 2).sum()

print(gini([50, 50]), round(gini([90, 10]), 2), gini([100, 0]))

# %% [markdown]
# ## Data: loan repayment (synthetic)

# %%
from sklearn.model_selection import train_test_split
rng = np.random.default_rng(12)
n = 1200
features = ["monthly_income_k", "existing_loans", "years_in_business", "age"]
df = pd.DataFrame({"monthly_income_k": rng.gamma(4, 15, n).round(1), "existing_loans": rng.poisson(1, n),
                   "years_in_business": rng.integers(0, 25, n), "age": rng.integers(21, 65, n)})
good = (df["monthly_income_k"] >= 60) & (df["existing_loans"] <= 1) | (df["years_in_business"] >= 8)
y = (good ^ (rng.random(n) < 0.08)).astype(int)
X_tr, X_te, y_tr, y_te = train_test_split(df[features], y, stratify=y, random_state=0)

# %% [markdown]
# ## Example 2 - a readable decision tree

# %%
from sklearn.tree import DecisionTreeClassifier, export_text
tree = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X_tr, y_tr)
print(export_text(tree, feature_names=features))
print("test accuracy:", round(tree.score(X_te, y_te), 3))

# %% [markdown]
# ## Example 3 - depth vs over-fitting

# %%
for d in [1, 3, 5, 10, None]:
    t = DecisionTreeClassifier(max_depth=d, random_state=0).fit(X_tr, y_tr)
    print(f"depth {str(d):>4}: train {t.score(X_tr, y_tr):.3f} | test {t.score(X_te, y_te):.3f}")

# %% [markdown]
# ## Example 4 - random forest and feature importance

# %%
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=300, random_state=0).fit(X_tr, y_tr)
imp = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=False)
print(imp.round(3)); print("forest test accuracy:", round(rf.score(X_te, y_te), 3))
assert imp.index[0] in ("monthly_income_k", "years_in_business")   # the real drivers come first

# %% [markdown]
# ## Example 5 - Naive Bayes for SMS spam

# %%
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.pipeline import make_pipeline
texts = ["You won a free prize call now", "Claim your free Rs 50000 reward today",
         "Urgent! your SIM wins lucky draw", "Free bundle offer click link",
         "Are we meeting at 5 near Tariq Road", "Please bring the notes for class",
         "Ammi says come home early", "Lecture moved to room 4 tomorrow"]
labels = ["spam"] * 4 + ["ham"] * 4
spam = make_pipeline(CountVectorizer(), MultinomialNB()).fit(texts, labels)
print(spam.predict(["Congratulations you won a free prize", "class notes for tomorrow"]))

# %% [markdown]
# ## Example 6 - SVM and cross-validated comparison

# %%
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
X, yy = df[features], y
models = {"tree": DecisionTreeClassifier(max_depth=4, random_state=0),
          "forest": RandomForestClassifier(200, random_state=0),
          "naive_bayes": GaussianNB(),
          "svm": make_pipeline(StandardScaler(), SVC(kernel="rbf", C=1))}
for name, m in models.items():
    print(f"{name:<12} CV accuracy {cross_val_score(m, X, yy, cv=5).mean():.3f}")
