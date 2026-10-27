"""Session 08 - generate the README image images/sales_dashboard.png (synthetic shop data)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

rng = np.random.default_rng(8)
months = np.arange(1, 13)
revenue = pd.Series(400 + 25 * months + rng.normal(0, 25, 12), index=months)
revenue[4] += 220          # an Eid spike in April
customers = (revenue / 4 + rng.normal(0, 8, 12)).round()
branch = pd.Series({"Clifton": 820, "Gulshan": 640, "DHA": 910, "Saddar": 450, "Johar": 560})
marks = rng.normal(62, 12, 200).clip(0, 100)

fig, axes = plt.subplots(2, 2, figsize=(11, 7), layout="constrained")
ax = axes[0, 0]
ax.plot(months, revenue, marker="o", label="Revenue")
peak = int(revenue.idxmax())
ax.annotate("Eid peak", xy=(peak, revenue[peak]), xytext=(peak + 1.5, revenue[peak] - 40),
            arrowprops={"arrowstyle": "->"})
ax.set(title="Monthly revenue vs customers", xlabel="Month", ylabel="Rs '000")
ax2 = ax.twinx(); ax2.plot(months, customers, color="orange", ls="--", label="Customers"); ax2.set_ylabel("Customers")
ax.grid(alpha=0.3)
order = branch.sort_values()
bars = axes[0, 1].barh(order.index, order.values, color="#2a9d8f")
axes[0, 1].bar_label(bars, padding=3); axes[0, 1].set_title("Sales by branch (Rs '000)")
axes[1, 0].hist(marks, bins=15, edgecolor="white")
axes[1, 0].axvline(marks.mean(), color="red", ls="--", label=f"mean {marks.mean():.1f}")
axes[1, 0].legend(); axes[1, 0].set_title("Customer satisfaction scores")
spend = rng.uniform(10, 100, 40); sales = (3 * spend + rng.normal(0, 30, 40)).clip(5)
axes[1, 1].scatter(spend, sales, c=spend, cmap="viridis", alpha=0.8)
axes[1, 1].set(title="Ad spend vs sales", xlabel="Ad spend (Rs '000)", ylabel="Sales (Rs '000)")
fig.suptitle("Shop dashboard (synthetic data)", fontsize=14)
fig.savefig("../images/sales_dashboard.png", dpi=110)
plt.close(fig)

# second image comes from the problem solution so the README shows its output
from problem_solution import make_class, results_dashboard
results_dashboard(make_class(), "../images/results_dashboard.png")
print("charts written")
