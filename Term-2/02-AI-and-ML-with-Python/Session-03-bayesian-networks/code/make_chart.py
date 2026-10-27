"""Session 03 - README image: how evidence changes P(LoadShedding)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from bn import example_net

net = example_net()
cases = {"no evidence": {}, "GeneratorOn": {"GeneratorOn": True},
         "GeneratorOn + UPSBeeps": {"GeneratorOn": True, "UPSBeeps": True},
         "GeneratorOn + UncleTesting": {"GeneratorOn": True, "UncleTesting": True}}
vals = [net.query("LoadShedding", ev)[True] for ev in cases.values()]
fig, ax = plt.subplots(figsize=(8, 3.8), layout="constrained")
ax.barh(list(cases), vals, color=["grey", "tab:blue", "tab:green", "tab:orange"])
for i, v in enumerate(vals):
    ax.text(v + 0.01, i, f"{v:.2f}", va="center")
ax.set(xlim=(0, 1.1), xlabel="P(LoadShedding = True | evidence)", title="Updating beliefs with evidence")
ax.invert_yaxis()
fig.savefig("../images/bayes.png", dpi=110); plt.close(fig)
print("saved bayes.png")
