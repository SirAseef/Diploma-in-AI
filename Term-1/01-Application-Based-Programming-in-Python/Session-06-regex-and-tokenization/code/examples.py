"""Session 06 - Regular Expressions and Tokenization: worked examples."""

# %% [markdown]
# ## Finding phone numbers and emails

# %%
import re
text = "Call 0300-1234567 or 021-34567890. Email: info@aptech.pk, admin@school.edu.pk"
print(re.findall(r"\b\d{3,4}-\d{7,8}\b", text))
print(re.findall(r"[\w.]+@[\w.]+\.\w+", text))

# %% [markdown]
# ## sub, split, groups, compile

# %%
print(re.sub(r"\d", "#", "PIN 4826"))
print(re.split(r"[,;]\s*", "red, green;blue"))
m = re.search(r"(\d{2})/(\d{2})/(\d{4})", "Exam on 15/11/2026")
day, month, year = m.groups()
print(day, month, year, "| span:", m.span())
cnic = re.compile(r"^\d{5}-\d{7}-\d$")
print(bool(cnic.fullmatch("42101-1234567-1")), bool(cnic.fullmatch("4210-1234567-1")))

# %% [markdown]
# ## match vs search, greedy vs lazy

# %%
print(re.match(r"AI", "Learn AI"), re.search(r"AI", "Learn AI"))
html = "<b>x</b><b>y</b>"
print(re.findall(r"<b>.*</b>", html), re.findall(r"<b>.*?</b>", html))

# %% [markdown]
# ## Comparing tokenizers

# %%
s = "Don't stop, AI-2026!"
print(s.split())
print(re.findall(r"\w+", s))
print(re.findall(r"[A-Za-z]+(?:'[a-z]+)?|\d+", s))
print(re.findall(r"\w+|[^\w\s]", s))
print(re.split(r"(?<=[.!?])\s+", "One. Two! Three?"))

# %% [markdown]
# ## Tokenize and count words

# %%
from collections import Counter
review = "The course is great. The labs are great and the teacher is great!"
tokens = re.findall(r"[a-z]+", review.lower())
stop = {"the", "is", "are", "and"}
print(Counter(t for t in tokens if t not in stop).most_common(3))
