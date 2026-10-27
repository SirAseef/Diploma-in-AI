"""Session 02 - Real-life problem: late-delivery prediction, linear vs neural network."""
import warnings
import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
warnings.filterwarnings("ignore", category=ConvergenceWarning)


def make_orders(n=600, seed=3):
    rng = np.random.default_rng(seed)
    dist = rng.uniform(1, 30, n)
    hour = rng.uniform(8, 22, n)
    rush = ((hour > 17) & (hour < 20)) | ((hour > 8) & (hour < 10))
    late = ((dist > 20) ^ rush).astype(int)
    flip = rng.random(n) < 0.05
    return np.column_stack([dist, hour]), np.where(flip, 1 - late, late)


def compare(X, y, seed=0):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=seed, stratify=y)
    models = {"logistic": LogisticRegression(),
              "mlp": MLPClassifier((16, 8), max_iter=2000, random_state=seed)}
    return {k: make_pipeline(StandardScaler(), m).fit(X_tr, y_tr).score(X_te, y_te) for k, m in models.items()}


if __name__ == "__main__":
    X, y = make_orders()
    print("late share:", y.mean().round(2))
    scores = compare(X, y)
    print({k: round(v, 3) for k, v in scores.items()})
    assert X.shape == (600, 2)
    assert scores["mlp"] > scores["logistic"] + 0.1, "network should capture the non-linear pattern"
    print("better model:", max(scores, key=scores.get))
