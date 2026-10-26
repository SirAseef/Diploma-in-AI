"""Session 05 - File and Exception Handling: worked examples.
All files are written into code/output/ (ignored by git)."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Setup: an output folder

# %%
from pathlib import Path
OUT = Path("output")
OUT.mkdir(exist_ok=True)

# %% [markdown]
# ## Example 1 - write, append, read

# %%
diary = OUT / "diary.txt"
with open(diary, "w", encoding="utf-8") as f:
    f.write("Day 1: learned variables\n")
with open(diary, "a", encoding="utf-8") as f:
    f.write("Day 2: learned loops\n")
with open(diary, encoding="utf-8") as f:
    for n, line in enumerate(f, 1):
        print(n, line.strip())
with open(diary, encoding="utf-8") as f:
    print(f.readline().strip(), "| position:", f.tell())
    f.seek(0)
    print(f.readlines())

# %% [markdown]
# ## Example 2 - CSV

# %%
import csv
rows = [["name", "marks"], ["Ali", 72], ["Sana", 91]]
with open(OUT / "marks.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)
with open(OUT / "marks.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["name"], int(row["marks"]))

# %% [markdown]
# ## Example 3 - JSON

# %%
import json
settings = {"theme": "dark", "font_size": 14}
with open(OUT / "settings.json", "w") as f:
    json.dump(settings, f, indent=2)
with open(OUT / "settings.json") as f:
    print(json.load(f)["theme"])

# %% [markdown]
# ## Example 4 - try / except / else / finally

# %%
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero")
        return None
    except TypeError as e:
        print("Bad input:", e)
        return None
    else:
        return result
    finally:
        print("safe_divide finished")


print(safe_divide(10, 4))
print(safe_divide(10, 0))
print(safe_divide("10", 2))

# %% [markdown]
# ## Example 5 - custom exceptions and missing files

# %%
class InvalidMarksError(Exception):
    """Marks must be between 0 and 100."""


def set_marks(m):
    if not 0 <= m <= 100:
        raise InvalidMarksError(f"{m} is out of range")
    return m


for m in (88, 120):
    try:
        print("saved", set_marks(m))
    except InvalidMarksError as e:
        print("Rejected:", e)

try:
    open(OUT / "does_not_exist.txt")
except FileNotFoundError as e:
    print("Handled:", e.__class__.__name__)
