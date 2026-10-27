"""Session 10 - README image: degree 1 vs 3 vs 15 polynomial fits."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

rng = np.random.default_rng(10)
x = np.sort(rng.uniform(0, 10, 30))
y = 3 + 2 * np.sin(x / 1.6) + 0.3 * x + rng.normal(0, 0.4, 30)
grid = np.linspace(0, 10, 400).reshape(-1, 1)
fig, axes = plt.subplots(1, 3, figsize=(13, 3.8), sharey=True, layout="constrained")
for ax, d, name in zip(axes, [1, 4, 15], ["under-fit (degree 1)", "good fit (degree 4)", "over-fit (degree 15)"]):
    m = make_pipeline(PolynomialFeatures(d), StandardScaler(), LinearRegression()).fit(x.reshape(-1, 1), y)
    ax.scatter(x, y, s=18, color="#264653")
    ax.plot(grid, np.clip(m.predict(grid), -2, 12), color="#e76f51", lw=2)
    ax.set(title=name, xlabel="x", ylim=(-1, 10))
axes[0].set_ylabel("y")
fig.savefig("../images/poly_fits.png", dpi=110)
plt.close(fig)
print("chart written")
