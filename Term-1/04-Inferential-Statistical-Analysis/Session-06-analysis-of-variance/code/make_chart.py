"""Session 06 - README image: groups with small vs large within-group spread."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

rng = np.random.default_rng(6)
means = [60, 66, 72]
fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True, layout="constrained")
for ax, sd, title in [(axes[0], 3, "Small within-group spread"), (axes[1], 14, "Large within-group spread")]:
    groups = [rng.normal(m, sd, 25) for m in means]
    for i, g in enumerate(groups):
        ax.scatter(np.full(g.size, i) + rng.uniform(-0.12, 0.12, g.size), g, s=14, alpha=0.7)
        ax.hlines(g.mean(), i - 0.25, i + 0.25, color="black", lw=2)
    f, p = stats.f_oneway(*groups)
    ax.set(title=f"{title}\nF = {f:.1f}, p = {p:.3g}", xticks=[0, 1, 2], xticklabels=["Method A", "Method B", "Method C"])
axes[0].set_ylabel("score")
fig.savefig("../images/anova_groups.png", dpi=110)
plt.close(fig)
print("chart written")
