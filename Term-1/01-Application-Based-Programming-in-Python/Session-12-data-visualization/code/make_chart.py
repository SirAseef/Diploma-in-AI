"""Generate the illustration images used in this session's README (saved to ../images/)."""
import matplotlib.pyplot as plt
import numpy as np

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [120, 135, 128, 160, 175, 190]

# 1. anatomy of a figure
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(months, sales, marker="o", color="#1f77b4", label="Shop A")
ax.plot(months, [100, 110, 125, 130, 150, 155], marker="s", color="#ff7f0e", label="Shop B")
ax.set_title("Title: Monthly sales (thousand Rs)")
ax.set_xlabel("x-label: month"); ax.set_ylabel("y-label: sales")
ax.legend(title="legend"); ax.grid(alpha=0.3)
ax.annotate("annotation", xy=(5, 190), xytext=(3, 182), arrowprops=dict(arrowstyle="->"))
fig.tight_layout(); fig.savefig("../images/anatomy.png", dpi=110); plt.close(fig)

# 2. gallery: which chart for which question
rng = np.random.default_rng(7)
fig, axs = plt.subplots(2, 3, figsize=(11, 6.5))
axs[0, 0].plot(months, sales, marker="o"); axs[0, 0].set_title("Line - trend over time")
axs[0, 1].bar(["Karachi", "Lahore", "Quetta", "Multan"], [42, 35, 12, 18], color="#2ca02c"); axs[0, 1].set_title("Bar - compare categories")
h = rng.normal(65, 12, 300); axs[0, 2].hist(h, bins=20, color="#9467bd", edgecolor="white"); axs[0, 2].set_title("Histogram - distribution")
x = rng.uniform(1, 10, 60); axs[1, 0].scatter(x, 8 * x + rng.normal(0, 8, 60), color="#d62728"); axs[1, 0].set_title("Scatter - relationship")
axs[1, 1].boxplot([rng.normal(60, 10, 80), rng.normal(70, 6, 80), rng.normal(55, 15, 80)])
axs[1, 1].set_xticks([1, 2, 3], ["Sec A", "Sec B", "Sec C"]); axs[1, 1].set_title("Box - spread & outliers")
axs[1, 2].pie([45, 30, 25], labels=["Mobile", "Laptop", "Tablet"], autopct="%1.0f%%"); axs[1, 2].set_title("Pie - parts of a whole")
fig.tight_layout(); fig.savefig("../images/chart_gallery.png", dpi=100); plt.close(fig)
print("images written")
