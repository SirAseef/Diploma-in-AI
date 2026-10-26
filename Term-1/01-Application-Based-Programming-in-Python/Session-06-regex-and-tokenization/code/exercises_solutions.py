"""Session 06 practice solutions."""
import re

tags = re.findall(r"#\w+", "Loving #Python and #AI at #Aptech2026!")
print(tags)
assert tags == ["#Python", "#AI", "#Aptech2026"]


def valid_mobile(s):
    return re.fullmatch(r"03\d{2}-\d{7}", s) is not None


assert valid_mobile("0312-3456789") and not valid_mobile("0412-3456789") and not valid_mobile("0312-345678")

fixed = re.sub(r"\s+", " ", "too    many   spaces")
print(fixed)
assert fixed == "too many spaces"

para = "Python is easy. Regex is powerful! Are you ready?"
for s in re.split(r"(?<=[.!?])\s+", para):
    print(len(re.findall(r"\w+", s)), "words:", s)
