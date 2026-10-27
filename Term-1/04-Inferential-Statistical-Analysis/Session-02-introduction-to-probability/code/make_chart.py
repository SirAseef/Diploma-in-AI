"""Session 02 - README image: binomial, Poisson and normal distributions."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

fig, axes = plt.subplots(1, 3, figsize=(13, 3.6), layout="constrained")
k = np.arange(0, 21)
axes[0].bar(k, stats.binom(20, 0.3).pmf(k), color="#219ebc")
axes[0].set(title="Binomial(n=20, p=0.3)", xlabel="successes", ylabel="probability")
k2 = np.arange(0, 16)
axes[1].bar(k2, stats.poisson(4).pmf(k2), color="#fb8500")
axes[1].set(title="Poisson(λ=4)", xlabel="events per interval")
x = np.linspace(130, 206, 400); d = stats.norm(168, 7)
axes[2].plot(x, d.pdf(x), color="#023047")
for s, a in [(3, 0.15), (2, 0.25), (1, 0.4)]:
    xs = np.linspace(168 - s * 7, 168 + s * 7, 200)
    axes[2].fill_between(xs, d.pdf(xs), alpha=a, color="#8ecae6")
axes[2].set(title="Normal(μ=168, σ=7): 68-95-99.7", xlabel="height (cm)")
fig.savefig("../images/distributions.png", dpi=110)
plt.close(fig)
print("chart written")
