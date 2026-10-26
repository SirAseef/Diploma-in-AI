"""Session 01 - Basics of Python: worked examples. Run: python examples.py"""

# %% [markdown]
# ## Example 1 - first program

# %%
print("Assalam-o-Alaikum, Python!")

# %% [markdown]
# ## Example 2 - variables and multiple assignment

# %%
name = "Ayesha"          # string
age = 19                 # integer
height_m = 1.62          # float
x, y, z = 1, 2, 3
a = b = 0
print(name, "is", age, "years old")
print(type(name), type(age), type(height_m))
print(x, y, z, a, b)

# %% [markdown]
# ## Example 3 - input and conversion
# `input()` always returns text. We use a fixed value here so the file runs without typing.

# %%
year_born = "2005"        # replace with: input("Which year were you born? ")
age = 2026 - int(year_born)
print(f"You are about {age} years old.")

# %% [markdown]
# ## Example 4 - indentation creates blocks

# %%
marks = 72
if marks >= 50:
    print("Pass")
    print("Well done")
print("Result printed")

# %% [markdown]
# ## Example 5 - Python's keywords

# %%
import keyword
print(len(keyword.kwlist), "keywords:", keyword.kwlist)
print("Is 'for' a keyword?", keyword.iskeyword("for"))
print("Is 'total' a valid identifier?", "total".isidentifier())
print("Is '2total' a valid identifier?", "2total".isidentifier())
