# Session 02 · NumPy Library

> **Module:** Data Science with Python · **Term 1** · ⏱️ ~2 hours
> **You will learn:** what a NumPy `ndarray` is, how to create, reshape, index and slice arrays, vectorised maths and broadcasting, boolean masks, aggregation along axes, and random numbers for simulation.

---

## 1. Why NumPy?

A Python list can hold anything, so every element carries extra baggage and loops are slow. A NumPy **array** stores numbers of one type in one block of memory, and its operations run in compiled C code. That makes it 10–100× faster and lets you write maths on whole columns at once.

> 📒 **Analogy:** A list is a *rickshaw* — flexible, goes anywhere, carries anything, one trip at a time. A NumPy array is the *Green Line bus* — fixed route, everyone the same type of passenger, but it moves hundreds at once.

```mermaid
flowchart TD
    L[Python list<br/>mixed types · loops] -->|np.array| A[ndarray<br/>one dtype · contiguous]
    A --> V[Vectorised maths<br/>a * 2, a + b]
    A --> M[Boolean masks<br/>a[a > 50]]
    A --> X[Aggregations<br/>sum · mean · axis=0/1]
    A --> R[Reshape / stack]
    A --> P[pandas & scikit-learn<br/>use arrays underneath]
```

## 2. Reference tables

| Create | Result |
|---|---|
| `np.array([1, 2, 3])` | from a list |
| `np.zeros((2, 3))`, `np.ones(4)` | filled arrays |
| `np.arange(0, 10, 2)` | `[0 2 4 6 8]` |
| `np.linspace(0, 1, 5)` | 5 evenly spaced values |
| `np.eye(3)` | identity matrix |
| `rng = np.random.default_rng(7)` | modern random generator |

| Attribute / method | Meaning |
|---|---|
| `a.shape`, `a.ndim`, `a.size`, `a.dtype` | dimensions, rank, element count, type |
| `a.reshape(2, 3)`, `a.ravel()`, `a.T` | change shape, flatten, transpose |
| `a.sum(axis=0)` | down the rows → one value per **column** |
| `a.mean(axis=1)` | across columns → one value per **row** |
| `np.where(cond, x, y)` | element-wise if/else |
| `np.vstack`, `np.hstack`, `np.concatenate` | join arrays |

| Indexing | Example (`a` is 2-D) |
|---|---|
| single element | `a[1, 2]` |
| row / column | `a[0]`, `a[:, 1]` |
| slice | `a[:2, 1:]` |
| fancy | `a[[0, 2]]` |
| boolean | `a[a > 50]` |

**Broadcasting rule:** shapes are compared from the right; dimensions must be equal or one of them must be 1. `(4, 3) + (3,)` works (the row is repeated); `(4, 3) + (4,)` fails — use `(4, 1)`.

## 3. Worked examples

Full runnable code: [`code/examples.py`](./code/examples.py) · notebook: [`notebook.ipynb`](./notebook.ipynb)

### Example 1 — list vs array
```python
import numpy as np
prices = [120, 250, 90]
print([p * 1.17 for p in prices])     # list: needs a loop
arr = np.array(prices)
print(arr * 1.17)                       # array: one expression (17% GST)
```

### Example 2 — shape, reshape, transpose
```python
marks = np.array([72, 85, 64, 91, 58, 77])
grid = marks.reshape(2, 3)          # 2 students × 3 subjects
print(grid.shape, grid.T.shape)
```

### Example 3 — indexing and boolean masks
```python
print(grid[1, 2], grid[:, 0])
print(marks[marks >= 70])                    # only high scores
print(np.where(marks >= 60, "pass", "fail"))
```

### Example 4 — aggregation along axes
```python
scores = np.array([[72, 85, 64], [91, 58, 77], [66, 70, 88]])
print("per subject:", scores.mean(axis=0))
print("per student:", scores.sum(axis=1))
print("best student index:", scores.sum(axis=1).argmax())
```

### Example 5 — broadcasting
```python
weights = np.array([0.5, 0.3, 0.2])          # subject weights
weighted = (scores * weights).sum(axis=1)    # (3,3) * (3,) works
centred = scores - scores.mean(axis=0)       # subtract each column mean
```

### Example 6 — random simulation
```python
rng = np.random.default_rng(42)
dice = rng.integers(1, 7, size=10_000)
print(np.bincount(dice)[1:] / dice.size)     # each face ≈ 0.167
```

## 4. Common mistakes

| Mistake | Fix |
|---|---|
| Looping over an array element by element | Use vectorised expressions (`a * 2`, `np.sqrt(a)`) |
| `b = a` then changing `b` changes `a` | Slices and assignments are **views**; use `a.copy()` |
| Confusing `axis=0` and `axis=1` | `axis=0` collapses rows (gives per-column results) |
| `a > 5 and a < 10` raises an error | Use `(a > 5) & (a < 10)` with brackets |
| Integer array silently truncates `2.7` | Set `dtype=float` or use `astype(float)` |

## 5. Real-life coding problem 🧮

**Problem:** K-Electric records hourly electricity use (kWh) for 5 houses over 24 hours. Using a NumPy array of shape `(5, 24)`: find each house's monthly units (daily total × 30), the peak hour for the whole street, the houses above the street average, and the bill for each house if monthly units up to 200 cost Rs 22 and every unit above costs Rs 35 (slab billing done with `np.where`, no loops).

<details>
<summary>💡 Full solution</summary>

```python
import numpy as np

def street_report(usage, slab=200, low=22, high=35):
    daily = usage.sum(axis=1) * 30          # scale one day to a month
    peak_hour = int(usage.sum(axis=0).argmax())
    above = np.flatnonzero(daily > daily.mean())
    bill = np.where(daily <= slab, daily * low, slab * low + (daily - slab) * high)
    return daily, peak_hour, above, bill.round(0)
```
Full file with simulated data and checks: [`code/problem_solution.py`](./code/problem_solution.py)
</details>

## 6. Practice exercises

1. Create a 4×4 array of the numbers 1–16 and extract its main diagonal and the bottom-right 2×2 block.
2. Convert an array of Celsius temperatures to Fahrenheit and keep only values above 95 °F.
3. Standardise each column of a 2-D array: `(x - mean) / std` using broadcasting.
4. Simulate 1,000 tosses of a fair coin and estimate the probability of heads.

<details>
<summary>✅ Solutions</summary>

```python
import numpy as np
a = np.arange(1, 17).reshape(4, 4)
diag, block = np.diag(a), a[2:, 2:]

c = np.array([28, 33, 36, 40, 31])
f = c * 9 / 5 + 32
hot = f[f > 95]

def standardise(x):
    return (x - x.mean(axis=0)) / x.std(axis=0)

rng = np.random.default_rng(0)
p_heads = rng.integers(0, 2, 1000).mean()
```
File: [`code/exercises_solutions.py`](./code/exercises_solutions.py)
</details>

## 7. Quiz

1. Why are NumPy arrays faster than lists for maths?
2. What shape does `np.arange(12).reshape(3, -1)` have?
3. For a `(5, 3)` array, what shape does `a.mean(axis=0)` return?
4. How do you combine two conditions in a boolean mask?
5. Why might changing a slice change the original array?

<details>
<summary>Answers</summary>

1. They hold one data type in contiguous memory and run operations in compiled code, with no Python loop · 2. `(3, 4)` · 3. `(3,)` — one value per column · 4. `(cond1) & (cond2)` (or `|` for OR), each in brackets · 5. Basic slices are views that share memory; use `.copy()` for an independent array.
</details>

## 8. Summary

- `ndarray` = fast, single-type, n-dimensional array; check `shape` and `dtype` first.
- Index with positions, slices, lists or boolean masks; slices are views.
- Vectorised maths and broadcasting remove loops; `axis` controls aggregation direction.
- `np.random.default_rng(seed)` gives repeatable simulations.

---
[⬅ Session 01](../Session-01-python-for-data-science/) · [Module home](../README.md) · [Session 03 ➡](../Session-03-pandas-series-and-dataframes/)

<sub>Original teaching material by Aseef Ahmed · not official Aptech courseware · CC BY-NC 4.0 (text) / MIT (code)</sub>
