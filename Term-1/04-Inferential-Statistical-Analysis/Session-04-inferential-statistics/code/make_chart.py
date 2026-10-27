"""Session 04 - README image: CLT - skewed population vs distribution of sample means."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(4)
population = rng.exponential(5000, 500_000)
fig, axes = plt.subplots(1, 3, figsize=(13, 3.6), layout="constrained")
axes[0].hist(population, bins=80, color="#adb5bd")
axes[0].set(title="Population: skewed bills (Rs)", xlabel="Rs")
for ax, n in zip(axes[1:], [5, 40]):
    means = rng.choice(population, (5000, n)).mean(axis=1)
    ax.hist(means, bins=60, color="#4361ee", alpha=0.85)
    ax.set(title=f"Means of samples, n = {n}\nSD = {means.std():,.0f} (σ/√n = {population.std() / np.sqrt(n):,.0f})",
           xlabel="sample mean (Rs)")
fig.savefig("../images/clt.png", dpi=110)
plt.close(fig)
print("chart written")
