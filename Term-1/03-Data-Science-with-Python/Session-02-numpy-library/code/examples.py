"""Session 02 - NumPy library: worked examples."""

# %% [markdown]
# ## Example 1 - list vs array

# %%
import numpy as np
prices = [120, 250, 90]
print([round(p * 1.17, 2) for p in prices])
arr = np.array(prices)
print(arr * 1.17, arr.dtype)

# %% [markdown]
# ## Example 2 - shape, reshape, transpose

# %%
marks = np.array([72, 85, 64, 91, 58, 77])
grid = marks.reshape(2, 3)
print(grid, grid.shape, grid.T.shape, grid.ndim, grid.size)

# %% [markdown]
# ## Example 3 - indexing and boolean masks

# %%
print(grid[1, 2], grid[:, 0])
print(marks[marks >= 70])
print(np.where(marks >= 60, "pass", "fail"))
print(marks[(marks > 60) & (marks < 80)])

# %% [markdown]
# ## Example 4 - aggregation along axes

# %%
scores = np.array([[72, 85, 64], [91, 58, 77], [66, 70, 88]])
print("per subject:", scores.mean(axis=0).round(1))
print("per student:", scores.sum(axis=1))
print("best student index:", scores.sum(axis=1).argmax())

# %% [markdown]
# ## Example 5 - broadcasting

# %%
weights = np.array([0.5, 0.3, 0.2])
weighted = (scores * weights).sum(axis=1)
centred = scores - scores.mean(axis=0)
print(weighted, centred.round(1), sep="\n")
assert np.allclose(centred.mean(axis=0), 0)

# %% [markdown]
# ## Example 6 - random simulation

# %%
rng = np.random.default_rng(42)
dice = rng.integers(1, 7, size=10_000)
freq = np.bincount(dice)[1:] / dice.size
print(freq.round(3))
assert abs(freq.mean() - 1 / 6) < 1e-9

# %% [markdown]
# ## Bonus - views vs copies

# %%
a = np.arange(5)
view, copy = a[:3], a[:3].copy()
view[0] = 99
print(a, copy)
