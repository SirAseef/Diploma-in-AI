"""Session 09 - Seaborn: worked examples."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Data (synthetic, generated locally)

# %%
import matplotlib.pyplot as plt
import seaborn as sns
from students_data import make_students
sns.set_theme(style="whitegrid")
df = make_students()
print(df.head())

# %% [markdown]
# ## Example 1 - distributions with hue

# %%
ax = sns.histplot(data=df, x="score", hue="campus", kde=True, element="step")
plt.show()

# %% [markdown]
# ## Example 2 - box vs violin

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
sns.boxplot(data=df, x="campus", y="score", ax=axes[0])
sns.violinplot(data=df, x="campus", y="score", hue="gender", split=True, ax=axes[1])
plt.show()

# %% [markdown]
# ## Example 3 - bar (mean with CI) and count

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
sns.barplot(data=df, x="campus", y="score", errorbar=("ci", 95), ax=axes[0])
sns.countplot(data=df, x="programme", hue="campus", ax=axes[1])
plt.show()
print(df.groupby("campus")["score"].mean().round(1))

# %% [markdown]
# ## Example 4 - relationships and a fitted line

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
sns.scatterplot(data=df, x="study_hours", y="score", hue="campus", size="attendance", ax=axes[0])
sns.regplot(data=df, x="study_hours", y="score", scatter_kws={"alpha": 0.4}, ax=axes[1])
plt.show()

# %% [markdown]
# ## Example 5 - correlation heatmap

# %%
corr = df[["study_hours", "attendance", "sleep", "score"]].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1)
plt.show()
assert corr.loc["study_hours", "score"] > 0.5

# %% [markdown]
# ## Example 6 - small multiples and pairplot

# %%
g = sns.relplot(data=df, x="study_hours", y="score", col="campus", hue="gender", height=3)
plt.show()
pg = sns.pairplot(df[["study_hours", "attendance", "score", "campus"]], hue="campus", corner=True, height=2)
plt.show()
