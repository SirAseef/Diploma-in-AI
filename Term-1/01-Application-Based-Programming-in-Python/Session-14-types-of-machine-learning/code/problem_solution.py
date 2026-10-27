"""Real-life problem: one dataset, two kinds of ML.
An online store wants (a) to predict whether a visitor will buy (supervised) and
(b) to find natural shopper segments for marketing (unsupervised)."""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def make_sessions(n=600, seed=7):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "pages_viewed": rng.poisson(6, n),
        "minutes_on_site": rng.gamma(2, 4, n).round(1),
        "items_in_cart": rng.poisson(1.2, n),
        "returning": rng.integers(0, 2, n),
    })
    score = 0.25 * df.pages_viewed + 0.1 * df.minutes_on_site + 1.2 * df.items_in_cart + 0.8 * df.returning
    df["bought"] = (score + rng.normal(0, 1, n) > 4.5).astype(int)
    return df


def supervised_part(df):
    X, y = df.drop(columns="bought"), df["bought"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
    model = RandomForestClassifier(n_estimators=200, random_state=0).fit(X_tr, y_tr)
    acc = accuracy_score(y_te, model.predict(X_te))
    baseline = max(y_te.mean(), 1 - y_te.mean())       # always guess the majority class
    importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    return acc, baseline, importance


def unsupervised_part(df, k=3):
    feats = df[["pages_viewed", "minutes_on_site", "items_in_cart"]]
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(StandardScaler().fit_transform(feats))
    profile = feats.assign(segment=km.labels_).groupby("segment").mean().round(1)
    profile["size"] = pd.Series(km.labels_).value_counts().sort_index()
    return profile


if __name__ == "__main__":
    df = make_sessions()
    acc, base, imp = supervised_part(df)
    print(f"buy-prediction accuracy {acc:.2f} vs baseline {base:.2f}")
    print(imp.round(3))
    assert acc > base
    print(unsupervised_part(df))
    print("both parts OK")
