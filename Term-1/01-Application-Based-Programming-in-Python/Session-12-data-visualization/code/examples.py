"""Session 12 - Data Visualization in Python: worked examples.
Charts are saved into code/output/ (ignored by git)."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - your first line chart (pyplot style)

# %%
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
OUT = Path("output"); OUT.mkdir(exist_ok=True)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [120, 135, 128, 160, 175, 190]
plt.plot(months, sales, marker="o", color="teal", linestyle="--", label="Sales")
plt.title("Monthly sales (thousand Rs)")
plt.xlabel("Month"); plt.ylabel("Sales")
plt.legend(); plt.grid(alpha=0.3)
plt.savefig(OUT / "line.png", dpi=100)
plt.show()

# %% [markdown]
# ## Example 2 - bar chart with the object-oriented style (fig, ax)

# %%
cities = ["Karachi", "Lahore", "Islamabad", "Quetta"]
students = [42, 35, 20, 12]
fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(cities, students, color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"])
ax.bar_label(bars)                      # numbers on top of the bars
ax.set_title("Students per city"); ax.set_ylabel("Students")
fig.savefig(OUT / "bar.png", dpi=100)
plt.show()

# %% [markdown]
# ## Example 3 - histogram and box plot of marks

# %%
rng = np.random.default_rng(42)
marks = np.clip(rng.normal(66, 12, 200), 0, 100)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.hist(marks, bins=15, color="slateblue", edgecolor="white")
ax1.axvline(marks.mean(), color="red", linestyle="--", label=f"mean {marks.mean():.1f}")
ax1.set_title("Distribution of marks"); ax1.legend()
ax2.boxplot(marks, orientation="horizontal")
ax2.set_title("Same marks as a box plot")
fig.tight_layout(); fig.savefig(OUT / "hist_box.png", dpi=100)
plt.show()

# %% [markdown]
# ## Example 4 - scatter plot: study hours vs marks

# %%
hours = rng.uniform(0, 10, 50)
score = 35 + 6 * hours + rng.normal(0, 6, 50)
fig, ax = plt.subplots(figsize=(6, 4))
sc = ax.scatter(hours, score, c=score, cmap="viridis", s=40)
fig.colorbar(sc, label="score")
ax.set_xlabel("Study hours per week"); ax.set_ylabel("Exam score")
ax.set_title(f"Correlation r = {np.corrcoef(hours, score)[0, 1]:.2f}")
fig.savefig(OUT / "scatter.png", dpi=100)
plt.show()

# %% [markdown]
# ## Example 5 - plotting straight from a pandas DataFrame

# %%
df = pd.DataFrame({
    "month": months,
    "online": [50, 62, 58, 80, 95, 110],
    "shop": [70, 73, 70, 80, 80, 80],
}).set_index("month")
ax = df.plot(kind="bar", stacked=True, figsize=(6, 4), title="Online vs in-shop sales")
ax.set_ylabel("thousand Rs")
plt.tight_layout(); plt.savefig(OUT / "stacked.png", dpi=100)
plt.show()
print(df.sum())

# %% [markdown]
# ## Example 6 - a 2x2 dashboard with subplots

# %%
fig, axs = plt.subplots(2, 2, figsize=(10, 7))
axs[0, 0].plot(months, sales, marker="o"); axs[0, 0].set_title("Trend")
axs[0, 1].bar(cities, students); axs[0, 1].set_title("Compare")
axs[1, 0].hist(marks, bins=12); axs[1, 0].set_title("Distribution")
axs[1, 1].pie([45, 30, 25], labels=["Mobile", "Laptop", "Tablet"], autopct="%1.0f%%")
axs[1, 1].set_title("Share")
fig.suptitle("Mini dashboard", fontsize=14)
fig.tight_layout(); fig.savefig(OUT / "dashboard.png", dpi=100)
plt.show()
print(sorted(p.name for p in OUT.glob("*.png")))
