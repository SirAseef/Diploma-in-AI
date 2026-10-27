"""Session 01 - Basics of Python for data science: worked examples."""

# %% [markdown]
# ## Example 1 - records as a list of dicts

# %%
students = [
    {"name": "Ali", "city": "Karachi", "marks": 72},
    {"name": "Sana", "city": "Lahore", "marks": 91},
    {"name": "Hamza", "city": "Karachi", "marks": 48},
    {"name": "Ayesha", "city": "Islamabad", "marks": 66},
]
for s in students:
    print(f"{s['name']:<7} {s['city']:<10} {s['marks']}")

# %% [markdown]
# ## Example 2 - comprehensions

# %%
marks = [s["marks"] for s in students]
passed = [s["name"] for s in students if s["marks"] >= 50]
curved = [min(100, round(m * 1.05)) for m in marks]
print(marks, passed, curved)

# %% [markdown]
# ## Example 3 - quick statistics

# %%
import statistics as st
print("mean", st.mean(marks), "median", st.median(marks), "stdev", round(st.stdev(marks), 2))

# %% [markdown]
# ## Example 4 - counting and grouping

# %%
from collections import Counter, defaultdict
print(Counter(s["city"] for s in students).most_common())
by_city = defaultdict(list)
for s in students:
    by_city[s["city"]].append(s["marks"])
print({c: sum(v) / len(v) for c, v in by_city.items()})

# %% [markdown]
# ## Example 5 - sorting with lambda

# %%
top = sorted(students, key=lambda s: s["marks"], reverse=True)
print([s["name"] for s in top])

# %% [markdown]
# ## Example 6 - a reusable cleaning function

# %%
def to_float(value, default=None):
    """Turn messy text like ' 72 ', '72.5' or 'absent' into a float or default."""
    try:
        return float(str(value).strip())
    except ValueError:
        return default

raw = [" 72 ", "72.5", "absent", 90]
print([to_float(v) for v in raw])
assert to_float("absent") is None and to_float(" 8 ") == 8.0
