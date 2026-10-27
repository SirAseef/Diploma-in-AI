"""Session 10 - Practice exercise solutions."""
import numpy as np
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures


def rmse(y_true, y_pred):
    return float(np.sqrt(np.mean((np.asarray(y_true) - np.asarray(y_pred)) ** 2)))


if __name__ == "__main__":
    rng = np.random.default_rng(1)
    x = rng.uniform(-3, 3, 150); y = x ** 3 - 4 * x + rng.normal(0, 1, 150)
    X_tr, X_te, y_tr, y_te = train_test_split(x.reshape(-1, 1), y, random_state=0)
    r2 = {d: r2_score(y_te, make_pipeline(PolynomialFeatures(d), LinearRegression()).fit(X_tr, y_tr).predict(X_te))
          for d in (2, 3)}
    print("test R2:", {k: round(v, 3) for k, v in r2.items()})
    assert r2[3] > r2[2]

    xe = np.linspace(0, 20, 40); ye = 5 * np.exp(0.12 * xe) * rng.normal(1, 0.03, 40)
    (a, b), _ = curve_fit(lambda t, a, b: a * np.exp(b * t), xe, ye, p0=[1, 0.1])
    assert abs(b - 0.12) < 0.01

    area = rng.uniform(400, 4000, 100); price = 7000 * area ** 0.9 * rng.normal(1, 0.05, 100)
    bpow = LinearRegression().fit(np.log(area).reshape(-1, 1), np.log(price)).coef_[0]
    assert abs(bpow - 0.9) < 0.05

    xs = rng.uniform(0, 5, 80); ys = 2 * xs ** 2 + rng.normal(0, 1, 80); Xs = xs.reshape(-1, 1)
    r_lin = rmse(ys, LinearRegression().fit(Xs, ys).predict(Xs))
    r_quad = rmse(ys, make_pipeline(PolynomialFeatures(2), LinearRegression()).fit(Xs, ys).predict(Xs))
    assert r_quad < r_lin and rmse([1, 2], [1, 4]) == np.sqrt(2)
    print("All exercise checks passed")
