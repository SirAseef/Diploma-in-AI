"""Session 13 - README image: confusion matrix + ROC curve."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=1500, n_features=6, n_informative=4, weights=[0.85], random_state=13)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, stratify=y, random_state=0)
m = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.3), layout="constrained")
ConfusionMatrixDisplay.from_estimator(m, X_te, y_te, display_labels=["negative", "positive"], cmap="Blues", ax=axes[0])
axes[0].set_title("Confusion matrix (threshold 0.5)")
RocCurveDisplay.from_estimator(m, X_te, y_te, ax=axes[1], name="logistic regression")
axes[1].plot([0, 1], [0, 1], "k--", label="random (AUC 0.5)"); axes[1].legend(loc="lower right")
axes[1].set_title("ROC curve")
fig.savefig("../images/evaluation.png", dpi=110)
plt.close(fig)
print("chart written")
