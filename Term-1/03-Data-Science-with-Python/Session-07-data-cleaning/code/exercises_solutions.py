"""Session 07 - Practice exercise solutions."""
import numpy as np
import pandas as pd


def missing_report(df):
    return df.isna().sum(), round(100 * df.isna().any(axis=1).mean(), 1)


def clean_gender(s):
    return s.str.strip().str.lower().str[0].map({"m": "Male", "f": "Female"})


def fill_temps(temps):
    return temps.ffill().fillna(temps.mean())


def iqr_outliers(values):
    s = pd.Series(values)
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    return s[(s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)].tolist()


if __name__ == "__main__":
    df = pd.DataFrame({"a": [1, None, 3, 4], "b": ["x", "y", None, "z"]})
    counts, pct = missing_report(df)
    assert counts.tolist() == [1, 1] and pct == 50.0
    assert clean_gender(pd.Series(["M", "male", " Female", "f", "F "])).tolist() == ["Male", "Male", "Female", "Female", "Female"]
    t = fill_temps(pd.Series([np.nan, 30.0, np.nan, 34.0]))
    assert t.tolist() == [32.0, 30.0, 30.0, 34.0]
    assert iqr_outliers([45, 48, 50, 52, 47, 49, 120, 51, 5]) == [120, 5]
    print("All exercise checks passed")
