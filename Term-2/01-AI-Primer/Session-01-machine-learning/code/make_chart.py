"""Session 01 - README image: traditional programming vs machine learning, and overfitting curve."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

fig, axes = plt.subplots(1, 2, figsize=(12, 4), layout="constrained")
ax = axes[0]; ax.axis("off")
ax.set_title("Traditional programming vs machine learning")
for y, (a, b, c) in zip([0.7, 0.25], [("Rules + Data", "Program", "Answers"), ("Data + Answers", "Learning", "Rules (model)")]):
    for x, t in zip([0.12, 0.5, 0.88], (a, b, c)):
        ax.text(x, y, t, ha="center", va="center", fontsize=11,
                bbox=dict(boxstyle="round", fc="#e8f0fe" if x != 0.5 else "#fde68a"))
    ax.annotate("", (0.38, y), (0.25, y), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", (0.75, y), (0.62, y), arrowprops=dict(arrowstyle="->"))
X, y = make_classification(600, n_features=10, n_informative=4, flip_y=0.1, random_state=0)
Xa, Xb, ya, yb = train_test_split(X, y, random_state=0)
d = range(1, 16)
tr = [DecisionTreeClassifier(max_depth=k, random_state=0).fit(Xa, ya).score(Xa, ya) for k in d]
te = [DecisionTreeClassifier(max_depth=k, random_state=0).fit(Xa, ya).score(Xb, yb) for k in d]
axes[1].plot(d, tr, marker="o", label="train"); axes[1].plot(d, te, marker="s", label="test")
axes[1].set(title="Overfitting: train vs test accuracy", xlabel="tree depth", ylabel="accuracy"); axes[1].legend()
fig.savefig("../images/ml_overview.png", dpi=110); plt.close(fig)
print("saved ml_overview.png")
