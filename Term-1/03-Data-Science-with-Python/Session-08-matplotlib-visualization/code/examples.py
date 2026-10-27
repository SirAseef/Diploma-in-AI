"""Session 08 - Matplotlib: worked examples."""

# %% [markdown]
# ## Data

# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
rng = np.random.default_rng(8)
months = np.arange(1, 13)
revenue = pd.Series(400 + 25 * months + rng.normal(0, 25, 12), index=months)
revenue[4] += 220
customers = (revenue / 4).round()

# %% [markdown]
# ## Example 1 - the object-oriented pattern

# %%
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(months, revenue, marker="o", label="Revenue")
ax.set(title="Monthly revenue (Rs '000)", xlabel="Month", ylabel="Rs '000")
ax.legend(); ax.grid(alpha=0.3)
plt.show()

# %% [markdown]
# ## Example 2 - sorted horizontal bars with labels

# %%
branch_sales = pd.Series({"Clifton": 820, "Gulshan": 640, "DHA": 910, "Saddar": 450})
fig, ax = plt.subplots(figsize=(6, 3))
order = branch_sales.sort_values()
bars = ax.barh(order.index, order.values, color="#2a9d8f")
ax.bar_label(bars, fmt="%.0f", padding=3)
plt.show()

# %% [markdown]
# ## Example 3 - histogram with a mean line

# %%
marks = pd.Series(rng.normal(62, 12, 200).clip(0, 100))
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.hist(marks, bins=15, edgecolor="white")
ax.axvline(marks.mean(), color="red", linestyle="--", label=f"mean {marks.mean():.1f}")
ax.legend(); plt.show()

# %% [markdown]
# ## Example 4 - scatter with colour and size

# %%
df = pd.DataFrame({"ad_spend": rng.uniform(10, 100, 40), "branch_code": rng.integers(0, 4, 40),
                   "staff": rng.integers(2, 10, 40)})
df["sales"] = 3 * df["ad_spend"] + rng.normal(0, 30, 40)
fig, ax = plt.subplots(figsize=(6, 4))
sc = ax.scatter(df["ad_spend"], df["sales"], c=df["branch_code"], s=df["staff"] * 15, cmap="viridis", alpha=0.7)
fig.colorbar(sc, ax=ax, label="branch")
plt.show()

# %% [markdown]
# ## Example 5 - a 2x2 dashboard with annotation and twin axis

# %%
fig, axes = plt.subplots(2, 2, figsize=(11, 7), layout="constrained")
axes[0, 0].plot(months, revenue)
peak = int(revenue.idxmax())
axes[0, 0].annotate("Eid peak", xy=(peak, revenue[peak]), xytext=(peak + 2, revenue[peak]),
                    arrowprops={"arrowstyle": "->"})
ax2 = axes[0, 0].twinx(); ax2.plot(months, customers, color="orange")
axes[0, 1].bar(branch_sales.index, branch_sales.values)
axes[1, 0].hist(marks, bins=15)
axes[1, 1].scatter(df["ad_spend"], df["sales"])
plt.show()
assert peak == 4

# %% [markdown]
# ## Example 6 - box plots to compare groups

# %%
riders = ["Kashif", "Naveed", "Zubair"]
times = [rng.normal(m, 4, 50) for m in (28, 35, 22)]
fig, ax = plt.subplots(figsize=(6, 3))
ax.boxplot(times, tick_labels=riders, orientation="horizontal")
ax.set_xlabel("Delivery minutes")
plt.show()
