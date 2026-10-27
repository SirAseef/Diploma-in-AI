"""Session 10 - Real-life problem: most fuel-efficient truck speed via polynomial regression."""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


def best_speed(speed, fuel, degrees=range(1, 7), seed=0):
    X = speed.reshape(-1, 1)
    X_tr, X_te, y_tr, y_te = train_test_split(X, fuel, test_size=0.25, random_state=seed)
    X_fit, X_val, y_fit, y_val = train_test_split(X_tr, y_tr, test_size=0.25, random_state=seed)
    scores = {}
    for d in degrees:
        m = make_pipeline(PolynomialFeatures(d), StandardScaler(), LinearRegression()).fit(X_fit, y_fit)
        scores[d] = np.sqrt(mean_squared_error(y_val, m.predict(X_val)))
    d = min(scores, key=scores.get)
    model = make_pipeline(PolynomialFeatures(d), StandardScaler(), LinearRegression()).fit(X_tr, y_tr)
    grid = np.linspace(speed.min(), speed.max(), 500).reshape(-1, 1)
    sweet = float(grid[model.predict(grid).argmin(), 0])
    return d, r2_score(y_te, model.predict(X_te)), sweet, scores


if __name__ == "__main__":
    rng = np.random.default_rng(42)
    speed = rng.uniform(20, 120, 200)
    fuel = 22 + 600 / speed + 0.0022 * (speed - 40) ** 2 + rng.normal(0, 0.6, 200)
    d, r2, sweet, scores = best_speed(speed, fuel)
    print({k: round(v, 3) for k, v in scores.items()})
    print(f"chosen degree {d}, test R2 {r2:.3f}, sweet-spot speed {sweet:.0f} km/h")
    true_grid = np.linspace(20, 120, 2001)
    true_best = true_grid[(22 + 600 / true_grid + 0.0022 * (true_grid - 40) ** 2).argmin()]
    assert d >= 2
    assert r2 > 0.9
    assert abs(sweet - true_best) < 10
    print("true optimum:", round(true_best), "km/h - All checks passed")
