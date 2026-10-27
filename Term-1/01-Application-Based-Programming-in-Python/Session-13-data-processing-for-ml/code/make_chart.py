"""Generate README illustrations for Session 13 (saved to ../images/)."""
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(3)
salary = rng.normal(80_000, 20_000, 200)          # rupees (thousands scale)
age = rng.normal(30, 6, 200)

def minmax(x): return (x - x.min()) / (x.max() - x.min())
def zscore(x): return (x - x.mean()) / x.std()

fig, axs = plt.subplots(1, 3, figsize=(12, 3.8))
for ax, (title, f) in zip(axs, [("Raw values (log x-axis)", lambda x: x), ("Min-Max scaled (0 to 1)", minmax), ("Standardized (mean 0, sd 1)", zscore)]):
    ax.hist(f(age), bins=20, alpha=0.6, label="age")
    ax.hist(f(salary), bins=20, alpha=0.6, label="salary")
    ax.set_title(title); ax.legend()
axs[0].set_xscale("symlog")
fig.suptitle("Why scale? Raw salary dwarfs age; after scaling both share one range")
fig.tight_layout(); fig.savefig("../images/scaling.png", dpi=100); plt.close(fig)

# outliers via IQR
vals = np.concatenate([rng.normal(50, 8, 100), [110, 120, 5]])
q1, q3 = np.percentile(vals, [25, 75]); iqr = q3 - q1
lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
fig, ax = plt.subplots(figsize=(8, 2.8))
ax.boxplot(vals, orientation="horizontal", widths=0.5)
ax.axvline(lo, color="red", ls="--"); ax.axvline(hi, color="red", ls="--")
ax.text(lo, 1.35, f" lower fence {lo:.0f}", color="red"); ax.text(hi, 1.35, f" upper fence {hi:.0f}", color="red")
ax.set_title("IQR rule: points beyond Q1 - 1.5·IQR or Q3 + 1.5·IQR are outliers"); ax.set_yticks([])
fig.tight_layout(); fig.savefig("../images/iqr_outliers.png", dpi=100); plt.close(fig)
print("images written")
