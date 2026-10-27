"""Real-life problem: prepare a loan-application dataset for a machine-learning model."""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def make_applications(n=300, seed=0):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "income_k": rng.normal(90, 30, n).round(),
        "loan_k": rng.normal(400, 150, n).round(),
        "age": rng.integers(21, 60, n).astype(float),
        "city": rng.choice(["Karachi", "Lahore", "Islamabad", "Peshawar"], n),
        "employment": rng.choice(["salaried", "business", "freelance"], n),
    })
    df["approved"] = ((df["income_k"] * 5 > df["loan_k"]) & (df["age"] < 55)).astype(int)
    # make it messy
    df.loc[rng.choice(n, 20, replace=False), "income_k"] = np.nan
    df.loc[rng.choice(n, 10, replace=False), "city"] = None
    df.loc[[3, 7], "income_k"] = [2000, -50]         # data-entry errors
    df = pd.concat([df, df.head(5)], ignore_index=True)  # duplicates
    return df


def clean(df):
    df = df.drop_duplicates().copy()
    df.loc[(df["income_k"] <= 0) | (df["income_k"] > 1000), "income_k"] = np.nan  # impossible -> missing
    df["loan_to_income"] = df["loan_k"] / df["income_k"]
    return df


def build_preprocessor():
    num = ["income_k", "loan_k", "age", "loan_to_income"]
    cat = ["city", "employment"]
    return ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), num),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                          ("oh", OneHotEncoder(handle_unknown="ignore"))]), cat),
    ])


def prepare(df):
    df = clean(df)
    X, y = df.drop(columns="approved"), df["approved"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)
    prep = build_preprocessor()
    return prep.fit_transform(X_tr), prep.transform(X_te), y_tr, y_te, prep


if __name__ == "__main__":
    raw = make_applications()
    print("raw rows:", len(raw), "| missing:", int(raw.isna().sum().sum()))
    Xtr, Xte, ytr, yte, prep = prepare(raw)
    print("train", Xtr.shape, "test", Xte.shape)
    print(list(prep.get_feature_names_out()))
    assert not np.isnan(Xtr).any() and not np.isnan(Xte).any()
    assert Xtr.shape[1] == 4 + 4 + 3
    assert abs(Xtr[:, 0].mean()) < 1e-9          # scaled on train -> mean 0
    print("data ready for a model")
