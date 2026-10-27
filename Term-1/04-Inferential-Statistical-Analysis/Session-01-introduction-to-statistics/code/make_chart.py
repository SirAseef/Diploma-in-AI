"""Session 01 - README image: mean vs median for symmetric and skewed data."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(1)
sym = rng.normal(60, 10, 3000)
right = rng.gamma(2, 3000, 3000)
fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), layout="constrained")
for ax, data, title, unit in [(axes[0], sym, "Exam marks (symmetric)", "marks"),
                              (axes[1], right, "Electricity bills (right-skewed)", "Rs")]:
    ax.hist(data, bins=40, color="#8ecae6", edgecolor="white")
    ax.axvline(np.mean(data), color="#d62828", lw=2, label=f"mean {np.mean(data):,.0f}")
    ax.axvline(np.median(data), color="#023047", lw=2, ls="--", label=f"median {np.median(data):,.0f}")
    ax.set(title=title, xlabel=unit, ylabel="count"); ax.legend()
fig.savefig("../images/centre_and_spread.png", dpi=110)
plt.close(fig)
print("chart written")
