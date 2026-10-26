"""Session 04 - Functions, Modules and Packages: worked examples. Run from this code/ folder."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Recursion: factorial and digit sum

# %%
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def digit_sum(n):
    return n if n < 10 else n % 10 + digit_sum(n // 10)


print(factorial(4), factorial(10), digit_sum(2026))

# %% [markdown]
# ## Recursion over nested data

# %%
def count_files(folder):
    return sum(1 if v is None else count_files(v) for v in folder.values())


drive = {"notes.txt": None, "AI": {"lab1.py": None, "data": {"a.csv": None, "b.csv": None}}}
print(count_files(drive))

# %% [markdown]
# ## Caching recursive results

# %%
from functools import lru_cache


@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print([fib(i) for i in range(10)], fib(80))

# %% [markdown]
# ## Lambda with sorted, map and filter

# %%
students = [("Ali", 72), ("Sana", 91), ("Umer", 65)]
print(sorted(students, key=lambda s: s[1], reverse=True))
print(list(map(lambda m: m + 5, [60, 70])))
print(list(filter(lambda m: m >= 50, [45, 67, 30, 88])))

# %% [markdown]
# ## Standard-library modules

# %%
import math
import random as rnd
from statistics import mean

rnd.seed(1)
print(math.sqrt(81), mean([2, 4, 6]), rnd.randint(1, 6))

# %% [markdown]
# ## Using our own package `school`

# %%
from school.grades import letter_grade, gpa
from school.report import make_report

print(letter_grade(84), gpa([84, 71, 58]))
print(make_report("Sana", {"Python": 84, "SQL": 71, "Stats": 58}))
