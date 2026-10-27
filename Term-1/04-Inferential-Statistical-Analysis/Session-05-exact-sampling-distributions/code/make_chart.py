"""Session 05 - README image: t vs normal, chi-square and F densities."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

fig, axes = plt.subplots(1, 3, figsize=(13, 3.6), layout="constrained")
x = np.linspace(-4, 4, 400)
axes[0].plot(x, stats.norm.pdf(x), "k--", label="normal")
for df in (1, 3, 10):
    axes[0].plot(x, stats.t.pdf(x, df), label=f"t, df={df}")
axes[0].set_title("Student's t"); axes[0].legend()
x2 = np.linspace(0, 25, 400)
for df in (2, 4, 8, 12):
    axes[1].plot(x2, stats.chi2.pdf(x2, df), label=f"df={df}")
axes[1].set_title("Chi-square"); axes[1].legend()
x3 = np.linspace(0, 5, 400)
for d1, d2 in ((2, 10), (5, 20), (10, 30)):
    axes[2].plot(x3, stats.f.pdf(x3, d1, d2), label=f"F({d1}, {d2})")
axes[2].set_title("F distribution"); axes[2].legend()
fig.savefig("../images/exact_distributions.png", dpi=110)
plt.close(fig)
print("chart written")
