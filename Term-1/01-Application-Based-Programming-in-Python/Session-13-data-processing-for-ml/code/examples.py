"""Session 13 - Data Processing Techniques in Machine Learning: worked examples."""

# %% [markdown]
# ## Example 1 - a messy dataset and a first look

# %%
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

df = pd.DataFrame({
    "age": [22, 25, None, 31, 28, 45, 38, 29, 26, 120],
    "city": ["Karachi", "Lahore", "Karachi", None, "Quetta", "Lahore", "Karachi", "Karachi", "Lahore", "Quetta"],
    "education": ["BS", "MS", "BS", "PhD", "Inter", "MS", "BS", "MS", "Inter", "BS"],
    "salary_k": [60, 95, 70, 150, 40, 130, 110, None, 45, 80],
    "hired": [0, 1, 0, 1, 0, 1, 1, 1, 0, 0],
})
print(df.info())
print(df.isna().sum())

# %% [markdown]
# ## Example 2 - missing values: drop vs fill

# %%
print("rows if we drop:", len(df.dropna()), "of", len(df))
filled = df.copy()
filled["age"] = filled["age"].fillna(filled["age"].median())
filled["salary_k"] = filled["salary_k"].fillna(filled["salary_k"].mean())
filled["city"] = filled["city"].fillna(filled["city"].mode()[0])
print(filled.isna().sum().sum(), "missing values left")

# %% [markdown]
# ## Example 3 - outliers with the IQR rule

# %%
q1, q3 = filled["age"].quantile([0.25, 0.75]); iqr = q3 - q1
lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
print(f"fences: {lo:.1f} .. {hi:.1f}")
print(filled[(filled["age"] < lo) | (filled["age"] > hi)])
filled["age"] = filled["age"].clip(lo, hi)          # cap instead of deleting

# %% [markdown]
# ## Example 4 - encoding categories

# %%
print(pd.get_dummies(filled, columns=["city"], dtype=int).head(3))
edu_order = [["Inter", "BS", "MS", "PhD"]]
filled["edu_level"] = OrdinalEncoder(categories=edu_order).fit_transform(filled[["education"]])
print(filled[["education", "edu_level"]].drop_duplicates())

# %% [markdown]
# ## Example 5 - scaling numbers

# %%
nums = filled[["age", "salary_k"]]
print(pd.DataFrame(MinMaxScaler().fit_transform(nums), columns=nums.columns).round(2).head())
print(pd.DataFrame(StandardScaler().fit_transform(nums), columns=nums.columns).round(2).describe().loc[["mean", "std"]])

# %% [markdown]
# ## Example 6 - split FIRST, then fit the processing on training data only

# %%
X, y = df.drop(columns="hired"), df["hired"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
print(X_train.shape, X_test.shape)

# %% [markdown]
# ## Example 7 - one reusable Pipeline + ColumnTransformer

# %%
numeric = ["age", "salary_k"]
nominal = ["city"]
ordinal = ["education"]
prep = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
    ("nom", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                      ("onehot", OneHotEncoder(handle_unknown="ignore"))]), nominal),
    ("ord", OrdinalEncoder(categories=edu_order), ordinal),
])
Xtr = prep.fit_transform(X_train)        # learn medians, means, categories from TRAIN
Xte = prep.transform(X_test)             # only apply them to TEST
print(prep.get_feature_names_out())
print(np.round(Xtr, 2))
