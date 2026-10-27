"""Session 13 - Practice exercise solutions."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.tree import DecisionTreeClassifier

if __name__ == "__main__":
    tp, fp, fn, tn = 40, 10, 20, 130
    acc = (tp + tn) / 200; prec = tp / (tp + fp); rec = tp / (tp + fn)
    spec = tn / (tn + fp); f1 = 2 * prec * rec / (prec + rec)
    assert (acc, prec, round(rec, 3), round(spec, 3), round(f1, 3)) == (0.85, 0.8, 0.667, 0.929, 0.727)

    rng = np.random.default_rng(0)
    X, y = make_classification(n_samples=4000, weights=[0.95], n_informative=4, random_state=2)
    auc_random = roc_auc_score(y, rng.random(len(y)))
    assert abs(auc_random - 0.5) < 0.05

    res = cross_validate(DecisionTreeClassifier(max_depth=4, random_state=0), X, y,
                         cv=StratifiedKFold(5, shuffle=True, random_state=0), scoring=["recall", "f1"])
    print("tree recall", round(res["test_recall"].mean(), 3), "| f1", round(res["test_f1"].mean(), 3))

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, stratify=y, random_state=0)
    res = {}
    for cw in (None, "balanced"):
        p = RandomForestClassifier(class_weight=cw, max_depth=5, random_state=0).fit(X_tr, y_tr).predict(X_te)
        res[str(cw)] = (round(recall_score(y_te, p), 3), round(f1_score(y_te, p), 3))
    print("RF (recall, F1):", res)
    assert res["balanced"][0] > res["None"][0]
    print("All exercise checks passed")
