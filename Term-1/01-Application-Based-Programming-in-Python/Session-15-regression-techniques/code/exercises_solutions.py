"""Session 15 - practice exercise solutions."""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures


# 1. Fit y = m x + c with NumPy only (least squares formula)
def fit_line(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = ((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum()
    return m, y.mean() - m * x.mean()


# 2. Implement the metrics yourself
def metrics(y, p):
    y, p = np.asarray(y, float), np.asarray(p, float)
    err = y - p
    mae, mse = np.abs(err).mean(), (err ** 2).mean()
    r2 = 1 - (err ** 2).sum() / ((y - y.mean()) ** 2).sum()
    return {"MAE": mae, "MSE": mse, "RMSE": np.sqrt(mse), "R2": r2}


# 3. Choose the best polynomial degree (1..8) by 5-fold cross-validation
def best_degree(x, y):
    X = np.asarray(x).reshape(-1, 1)
    scores = {d: cross_val_score(make_pipeline(PolynomialFeatures(d), LinearRegression()), X, y, cv=5).mean()
              for d in range(1, 9)}
    return max(scores, key=scores.get)


# 4. Gradient descent for simple linear regression
def gradient_descent(x, y, lr=0.01, epochs=5000):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = c = 0.0
    for _ in range(epochs):
        p = m * x + c
        m -= lr * (-2 * (x * (y - p)).mean())
        c -= lr * (-2 * (y - p).mean())
    return m, c


if __name__ == "__main__":
    x = [1, 2, 3, 4, 5]; y = [3, 5, 7, 9, 11]
    print(fit_line(x, y)); assert np.allclose(fit_line(x, y), (2, 1))

    yt, yp = [10, 20, 30], [12, 18, 33]
    mt = metrics(yt, yp); print(mt); assert np.isclose(mt["R2"], r2_score(yt, yp))

    rng = np.random.default_rng(5)
    xs = rng.uniform(-3, 3, 80); ys = xs**3 - 2 * xs + rng.normal(0, 1, 80)
    d = best_degree(xs, ys); print("best degree:", d); assert d in (3, 4, 5)

    m, c = gradient_descent(x, y); print(round(m, 3), round(c, 3)); assert abs(m - 2) < 0.01 and abs(c - 1) < 0.05
    print("all exercise checks passed")
