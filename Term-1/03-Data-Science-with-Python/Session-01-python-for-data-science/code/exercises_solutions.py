"""Session 01 - Practice exercise solutions."""
from collections import Counter


def hot_days(temps):
    avg = sum(temps) / len(temps)
    return [i for i, t in enumerate(temps, 1) if t > avg]


def freq_sorted(text):
    return dict(Counter(text.split(",")).most_common())


def normalise(values):
    lo, hi = min(values), max(values)
    return [0.0 for _ in values] if hi == lo else [(v - lo) / (hi - lo) for v in values]


def group_names(pairs):
    out = {}
    for name, city in pairs:
        out.setdefault(city, []).append(name)
    return {c: sorted(n) for c, n in out.items()}


if __name__ == "__main__":
    assert hot_days([31, 34, 29, 36, 38, 33, 30]) == [2, 4, 5]
    assert freq_sorted("apple,banana,apple,mango,banana,apple") == {"apple": 3, "banana": 2, "mango": 1}
    assert normalise([10, 20, 30]) == [0.0, 0.5, 1.0]
    assert group_names([("Zara", "Lahore"), ("Ali", "Karachi"), ("Bina", "Lahore")]) == {"Lahore": ["Bina", "Zara"], "Karachi": ["Ali"]}
    print("All exercise checks passed")
