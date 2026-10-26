"""Session 03 - Introduction to Functions: worked examples."""

# %% [markdown]
# ## Anatomy of a function

# %%
def greet(name, greeting="Hello"):
    """Return a friendly greeting."""
    message = f"{greeting}, {name}!"
    return message


print(greet("Hamza"))
print(greet("Hamza", greeting="Salam"))
help(greet)

# %% [markdown]
# ## Example 1 - define, call, return

# %%
def circle_area(radius):
    return 3.14159 * radius ** 2


print(round(circle_area(5), 2))

# %% [markdown]
# ## Example 2 - default and keyword arguments

# %%
def power(base, exp=2):
    return base ** exp


print(power(4), power(2, 5), power(exp=3, base=10))

# %% [markdown]
# ## Example 3 - *args and **kwargs

# %%
def average(*marks):
    return sum(marks) / len(marks)


def student_card(name, **details):
    lines = [f"Name: {name}"] + [f"{k.title()}: {v}" for k, v in details.items()]
    return "\n".join(lines)


print(round(average(70, 85, 90), 2))
print(student_card("Zara", batch="2511C", course="AI"))

# %% [markdown]
# ## Example 4 - local vs global

# %%
counter = 0


def increment():
    global counter
    counter += 1


def show_local():
    counter = 99
    return counter


increment()
increment()
print(counter, show_local(), counter)

# %% [markdown]
# ## Example 5 - returning several values

# %%
def min_max(values):
    return min(values), max(values)


lo, hi = min_max([4, 9, 1, 7])
print(lo, hi)
