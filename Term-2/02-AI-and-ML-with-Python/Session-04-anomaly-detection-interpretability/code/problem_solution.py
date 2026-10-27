"""Session 04 - Real-life problem: card-fraud ranking with Isolation Forest plus plain-language reasons."""
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import average_precision_score

FEATURES = ["amount_pkr", "hour", "km_from_home", "merchant_risk_pct", "tx_last_hour"]


def make_transactions(n=3000, fraud_rate=0.015, seed=9):
    rng = np.random.default_rng(seed)
    X = np.column_stack([rng.lognormal(8, 0.6, n), rng.normal(15, 3.5, n).clip(0, 23),
                         rng.exponential(4, n), rng.beta(2, 8, n) * 100, rng.poisson(0.4, n)])
    y = np.zeros(n, int); k = int(n * fraud_rate)
    idx = rng.choice(n, k, replace=False); y[idx] = 1
    X[idx, 0] = rng.uniform(60000, 300000, k)
    X[idx, 1] = rng.choice([1, 2, 3, 4], k)
    X[idx, 2] = rng.uniform(30, 900, k)
    X[idx, 3] = rng.uniform(50, 95, k)
    X[idx, 4] = rng.integers(3, 9, k)
    return X, y


def rank(X, seed=0):
    iso = IsolationForest(n_estimators=300, contamination=0.015, random_state=seed).fit(np.log1p(X))
    return -iso.score_samples(np.log1p(X))


def reasons(X):
    med = np.median(X, axis=0)
    mad = np.median(np.abs(X - med), axis=0) * 1.4826
    mad[mad == 0] = 1.0

    def reason(row):
        rz = np.abs((row - med) / mad)
        top = np.argsort(-rz)[:2]
        return ", ".join(f"{FEATURES[i]}={row[i]:.0f} (typical {med[i]:.0f})" for i in top)
    return reason


if __name__ == "__main__":
    X, y = make_transactions()
    scores = rank(X)
    top30 = np.argsort(-scores)[:30]
    p30, ap = y[top30].mean(), average_precision_score(y, scores)
    print(f"precision@30 = {p30:.2f}, PR-AUC = {ap:.3f}, fraud cases = {y.sum()}")
    why = reasons(X)
    for i in top30[:3]:
        print(f"tx {i} (fraud={y[i]}): {why(X[i])}")
    assert p30 >= 0.8 and ap > 0.7
    print("OK")
