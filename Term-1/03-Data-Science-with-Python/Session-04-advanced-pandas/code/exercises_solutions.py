"""Session 04 - Practice exercise solutions."""
import pandas as pd


def top_per_batch(marks):
    return marks.loc[marks.groupby("batch")["marks"].idxmax(), ["batch", "student"]].reset_index(drop=True)


def pct_of_best(marks):
    m = marks.copy()
    m["pct_of_best"] = (100 * m["marks"] / m.groupby("batch")["marks"].transform("max")).round(1)
    return m


def only_in_one(a, b):
    m = a.merge(b, on="student", how="outer", indicator=True)
    return sorted(m.loc[m["_merge"] != "both", "student"])


def first_day_above(sales, limit=1000, window=7):
    roll = sales.rolling(window).mean()
    return roll[roll > limit].index[0]


if __name__ == "__main__":
    marks = pd.DataFrame({"batch": ["A", "A", "B", "B", "B"], "student": ["Ali", "Sana", "Hina", "Omar", "Zoya"],
                          "marks": [70, 85, 60, 90, 75]})
    assert top_per_batch(marks)["student"].tolist() == ["Sana", "Omar"]
    assert pct_of_best(marks)["pct_of_best"].tolist() == [82.4, 100.0, 66.7, 100.0, 83.3]
    a = pd.DataFrame({"student": ["Ali", "Sana", "Hina"]}); b = pd.DataFrame({"student": ["Sana", "Hina", "Omar"]})
    assert only_in_one(a, b) == ["Ali", "Omar"]
    sales = pd.Series([800, 900, 950, 1000, 1100, 1200, 1300, 1400],
                      index=pd.date_range("2026-10-01", periods=8))
    assert str(first_day_above(sales).date()) == "2026-10-07"
    print("All exercise checks passed")
