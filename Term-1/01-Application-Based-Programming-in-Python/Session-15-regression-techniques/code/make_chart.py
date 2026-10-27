"""Generate README illustrations for Session 15 (saved to ../images/)."""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

rng = np.random.default_rng(2)
x = np.sort(rng.uniform(0, 10, 25)); y = 2 + 1.5 * x - 0.12 * x**2 + rng.normal(0, 0.6, 25)
X = x.reshape(-1, 1); xs = np.linspace(0, 10, 300).reshape(-1, 1)

# best-fit line and residuals
lin = LinearRegression().fit(X, y)
fig, ax = plt.subplots(figsize=(6.5, 4))
ax.scatter(x, y, zorder=3, label="data")
ax.plot(xs, lin.predict(xs), "r-", label=f"ŷ = {lin.coef_[0]:.2f}x + {lin.intercept_:.2f}")
for xi, yi, pi in zip(x, y, lin.predict(X)):
    ax.plot([xi, xi], [yi, pi], color="grey", lw=0.8)
ax.set_title("Least squares: minimise the sum of squared residuals (grey)"); ax.legend()
fig.tight_layout(); fig.savefig("../images/least_squares.png", dpi=100); plt.close(fig)

# under / good / over fit
fig, axs = plt.subplots(1, 3, figsize=(13, 3.8), sharey=True)
for ax, d, t in zip(axs, [1, 2, 15], ["Degree 1 - underfit", "Degree 2 - good fit", "Degree 15 - overfit"]):
    m = make_pipeline(PolynomialFeatures(d), StandardScaler(), LinearRegression()).fit(X, y)
    ax.scatter(x, y); ax.plot(xs, np.clip(m.predict(xs), -2, 10), "r-"); ax.set_title(t); ax.set_ylim(-2, 10)
fig.tight_layout(); fig.savefig("../images/fit_comparison.png", dpi=100); plt.close(fig)
print("images written")
