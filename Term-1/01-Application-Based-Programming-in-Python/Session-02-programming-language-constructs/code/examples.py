"""Session 02 - Programming Language Constructs: worked examples."""

# %% [markdown]
# ## Data types and conversion

# %%
values = [42, 3.14, True, "Karachi", [90, 75], (24.86, 67.01), {"AI", "ML"}, {"name": "Sana"}]
for v in values:
    print(f"{str(v):22} -> {type(v).__name__}")
print(int("25") + 5, float("2.5") * 2, str(99) + "!")

# %% [markdown]
# ## Operators

# %%
print(17 // 5, 17 % 5, 2 ** 3, 10 / 2)
print(5 >= 3, True and False, not True)
print("a" in "cat", 3 in [1, 2, 3])
x = 10
x += 5
print(x)

# %% [markdown]
# ## Example 1 - if / elif / else

# %%
marks = 68
if marks >= 80:
    grade = "A"
elif marks >= 65:
    grade = "B"
elif marks >= 50:
    grade = "C"
else:
    grade = "F"
print(grade)

# %% [markdown]
# ## Example 2 & 3 - for loops

# %%
fruits = ["mango", "banana", "guava"]
for i, fruit in enumerate(fruits, start=1):
    print(i, fruit.title())

total = 0
for n in range(1, 11):
    total += n
print("Sum 1..10 =", total)

# %% [markdown]
# ## Example 4 - while with break / continue

# %%
n = 0
while True:
    n += 1
    if n % 2 == 0:
        continue
    if n > 9:
        break
    print(n, end=" ")
print()

# %% [markdown]
# ## Example 5 - dictionaries in loops

# %%
stock = {"pen": 40, "notebook": 0, "marker": 12}
for item, qty in stock.items():
    status = "OUT" if qty == 0 else "ok"
    print(f"{item:10} {qty:>3} {status}")

# %% [markdown]
# ## Example 6 - match statement

# %%
command = "stop"
match command:
    case "start":
        print("Engine on")
    case "stop":
        print("Engine off")
    case _:
        print("Unknown")
