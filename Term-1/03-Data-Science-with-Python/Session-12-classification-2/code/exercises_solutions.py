"""Session 12 - Practice exercise solutions."""
from sklearn.datasets import make_classification, make_moons
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

if __name__ == "__main__":
    g = 1 - (0.75 ** 2 + 0.25 ** 2)
    assert abs(g - 0.375) < 1e-12

    X, y = make_classification(n_samples=800, n_features=8, flip_y=0.1, random_state=1)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, random_state=0)
    leaf = {m: DecisionTreeClassifier(min_samples_leaf=m, random_state=0).fit(X_tr, y_tr).score(X_te, y_te) for m in (1, 10, 50)}
    print("min_samples_leaf ->", {k: round(v, 3) for k, v in leaf.items()})

    msgs = ["win cash prize now", "free recharge offer", "lucky draw winner claim", "cheap loan approved click",
            "see you at lunch", "assignment due friday", "call me after namaz", "bring biryani tonight"]
    labels = ["spam"] * 4 + ["ham"] * 4
    nb = make_pipeline(CountVectorizer(), MultinomialNB()).fit(msgs, labels)
    assert list(nb.predict(["claim your free prize", "lunch on friday"])) == ["spam", "ham"]

    Xm, ym = make_moons(400, noise=0.2, random_state=0)
    sv = {k: cross_val_score(make_pipeline(StandardScaler(), SVC(kernel=k)), Xm, ym, cv=5).mean() for k in ("linear", "rbf")}
    print("SVM on moons:", {k: round(v, 3) for k, v in sv.items()})
    assert sv["rbf"] > sv["linear"]
    print("All exercise checks passed")
