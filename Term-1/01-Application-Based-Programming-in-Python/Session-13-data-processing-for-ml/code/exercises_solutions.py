"""Session 13 - practice exercise solutions."""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


# 1. Fill numeric NaNs with the median and text NaNs with the most common value
def fill_missing(df):
    out = df.copy()
    for col in out.columns:
        if pd.api.types.is_numeric_dtype(out[col]):
            out[col] = out[col].fillna(out[col].median())
        else:
            out[col] = out[col].fillna(out[col].mode()[0])
    return out


# 2. Min-max scaling by hand, compare with scikit-learn
def min_max(values):
    a = np.asarray(values, dtype=float)
    return (a - a.min()) / (a.max() - a.min())


# 3. Remove rows whose value in `col` is an IQR outlier
def drop_outliers(df, col):
    q1, q3 = df[col].quantile([0.25, 0.75]); iqr = q3 - q1
    keep = df[col].between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)
    return df[keep]


# 4. Feature engineering: from a date of birth and join date make age and tenure (years)
def add_features(df, today="2026-10-27"):
    out = df.copy(); t = pd.Timestamp(today)
    out["age"] = ((t - pd.to_datetime(out["dob"])).dt.days // 365)
    out["tenure_years"] = ((t - pd.to_datetime(out["joined"])).dt.days / 365).round(1)
    out["is_senior"] = (out["tenure_years"] >= 5).astype(int)
    return out


if __name__ == "__main__":
    d = pd.DataFrame({"marks": [50, None, 70], "city": ["Karachi", None, "Karachi"]})
    f = fill_missing(d); print(f); assert f.isna().sum().sum() == 0 and f.loc[1, "marks"] == 60

    v = [10, 20, 30, 50]
    mine = min_max(v); sk = MinMaxScaler().fit_transform(np.array(v).reshape(-1, 1)).ravel()
    print(mine); assert np.allclose(mine, sk)

    s = pd.DataFrame({"price": [100, 110, 105, 98, 102, 900]})
    print(drop_outliers(s, "price")); assert 900 not in drop_outliers(s, "price")["price"].values

    e = pd.DataFrame({"dob": ["1999-08-30", "2003-01-15"], "joined": ["2019-09-01", "2024-02-01"]})
    print(add_features(e)); assert add_features(e)["is_senior"].tolist() == [1, 0]
    print("all exercise checks passed")
