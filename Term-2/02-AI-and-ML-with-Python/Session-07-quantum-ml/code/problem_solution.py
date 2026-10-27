"""Session 07 - Real-life problem: quantum kernel vs classical SVMs on a small crop-health dataset."""
# notebook: run-in-code-dir
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from qsim import quantum_kernel


def make_crop_data(n=120, seed=7):
    rng = np.random.default_rng(seed)
    moisture = rng.uniform(20, 80, n); chlorophyll = rng.uniform(10, 60, n)
    healthy = ((moisture - 50) ** 2 / 400 + (chlorophyll - 35) ** 2 / 225 < 1).astype(int)
    flip = rng.random(n) < 0.05
    return np.column_stack([moisture, chlorophyll]), np.where(flip, 1 - healthy, healthy)


def compare(seed=0):
    X, y = make_crop_data()
    Xs = MinMaxScaler((0, np.pi)).fit_transform(X)
    X_tr, X_te, y_tr, y_te = train_test_split(Xs, y, test_size=0.3, random_state=seed, stratify=y)
    return {"quantum_kernel": SVC(kernel="precomputed").fit(quantum_kernel(X_tr, X_tr), y_tr)
            .score(quantum_kernel(X_te, X_tr), y_te),
            "linear_svm": SVC(kernel="linear").fit(X_tr, y_tr).score(X_te, y_te),
            "rbf_svm": SVC(kernel="rbf").fit(X_tr, y_tr).score(X_te, y_te)}


if __name__ == "__main__":
    res = compare()
    print({k: round(float(v), 3) for k, v in res.items()})
    print("Honest note: on small classical data, the RBF SVM is a strong baseline.")
    assert res["rbf_svm"] > res["linear_svm"]
    assert all(0 <= v <= 1 for v in res.values())
    print("OK")
