"""Session 03 - README image: scatter plots with different correlations."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(3)
x = rng.normal(0, 1, 200)
cases = [("r ≈ +0.95", x + rng.normal(0, 0.3, 200)), ("r ≈ +0.5", x + rng.normal(0, 1.6, 200)),
         ("r ≈ 0", rng.normal(0, 1, 200)), ("r ≈ -0.8", -x + rng.normal(0, 0.75, 200)),
         ("r ≈ 0 but curved", x ** 2 + rng.normal(0, 0.3, 200))]
fig, axes = plt.subplots(1, 5, figsize=(16, 3.2), layout="constrained")
for ax, (title, y) in zip(axes, cases):
    r = np.corrcoef(x, y)[0, 1]
    ax.scatter(x, y, s=8, alpha=0.6, color="#3a86ff")
    ax.set_title(f"{title}\n(actual r = {r:.2f})", fontsize=10); ax.set_xticks([]); ax.set_yticks([])
fig.savefig("../images/correlation_examples.png", dpi=105)
plt.close(fig)
print("chart written")
