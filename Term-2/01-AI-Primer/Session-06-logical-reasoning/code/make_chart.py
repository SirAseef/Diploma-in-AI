"""Session 06 - README image: exponential growth of model checking."""
import matplotlib
matplotlib.use("Agg")
import time
import matplotlib.pyplot as plt
from logic import count_models

ns, times = list(range(4, 19, 2)), []
for n in ns:
    t0 = time.perf_counter(); count_models(n); times.append(time.perf_counter() - t0)
fig, axes = plt.subplots(1, 2, figsize=(11, 4), layout="constrained")
axes[0].plot(ns, [2 ** n for n in ns], marker="o"); axes[0].set_yscale("log")
axes[0].set(title="Models to check = 2^n", xlabel="number of symbols n", ylabel="models (log)")
axes[1].plot(ns, times, marker="s", color="tab:red"); axes[1].set_yscale("log")
axes[1].set(title="Measured time to enumerate", xlabel="number of symbols n", ylabel="seconds (log)")
fig.savefig("../images/logic.png", dpi=110); plt.close(fig)
print("saved logic.png")
