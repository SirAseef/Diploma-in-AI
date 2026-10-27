"""Session 03 - Practice exercise solutions."""
import pandas as pd


def hot_days(limit=35):
    t = pd.Series([33, 36, 38, 34, 31, 37, 35], index=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    return t[t > limit]


def most_valuable(p):
    p = p.copy()
    p["value"] = p["price"] * p["stock"]
    return p.loc[p["value"].idxmax(), "name"]


def every_second(df):
    return df.iloc[::2, :2]


def tidy_columns(df):
    return df.rename(columns=lambda c: c.strip().lower().replace(" ", "_"))


if __name__ == "__main__":
    assert list(hot_days().index) == ["Tue", "Wed", "Sat"]
    p = pd.DataFrame({"name": ["pen", "copy", "bag"], "price": [30, 120, 1500], "stock": [200, 80, 10]})
    assert most_valuable(p) == "bag"
    assert every_second(p).shape == (2, 2)
    assert list(tidy_columns(pd.DataFrame(columns=["Unit Price", " Qty "])).columns) == ["unit_price", "qty"]
    print("All exercise checks passed")
