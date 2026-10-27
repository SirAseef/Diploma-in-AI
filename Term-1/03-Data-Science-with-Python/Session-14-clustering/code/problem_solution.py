"""Session 14 - Real-life problem: supermarket loyalty-card segmentation."""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

FEATURES = ["visits_per_month", "avg_basket", "pct_discounted", "days_since_last_visit"]


def make_loyalty(seed=4):
    rng = np.random.default_rng(seed)
    specs = {  # visits, basket, pct_discounted, days_since, n
        "loyal": (10, 6500, 0.10, 4, 250),
        "deal": (5, 2200, 0.55, 8, 300),
        "risk": (1, 2500, 0.15, 60, 150),
        "regular": (4, 3000, 0.15, 10, 300),
    }
    parts = []
    for v, b, p, d, n in specs.values():
        parts.append(pd.DataFrame({"visits_per_month": rng.normal(v, 1.0, n).clip(0.2),
                                   "avg_basket": rng.normal(b, b * 0.12, n).round(0),
                                   "pct_discounted": rng.normal(p, 0.05, n).clip(0, 1),
                                   "days_since_last_visit": rng.normal(d, d * 0.25, n).clip(0).round(0)}))
    return pd.concat(parts, ignore_index=True)


def name_segment(row, overall):
    if row["days_since_last_visit"] > 1.5 * overall["days_since_last_visit"]:
        return "At risk"
    if row["pct_discounted"] > 1.3 * overall["pct_discounted"]:
        return "Deal seekers"
    if row["avg_basket"] > overall["avg_basket"] and row["visits_per_month"] > overall["visits_per_month"]:
        return "Loyal big spenders"
    return "Regulars"


def segment(df, k_range=range(2, 8)):
    X = StandardScaler().fit_transform(df[FEATURES])
    sil = {k: round(silhouette_score(X, KMeans(k, n_init=10, random_state=0).fit_predict(X)), 3) for k in k_range}
    k = max(sil, key=sil.get)
    out = df.copy()
    out["segment"] = KMeans(k, n_init=10, random_state=0).fit_predict(X)
    profile = out.groupby("segment")[FEATURES].mean().round(2)
    profile["size"] = out["segment"].value_counts().sort_index()
    profile["name"] = profile.apply(name_segment, axis=1, overall=df[FEATURES].mean())
    return k, sil, profile


if __name__ == "__main__":
    df = make_loyalty()
    k, sil, profile = segment(df)
    print("silhouette by k:", sil)
    print(profile)
    assert k == 4
    assert sorted(profile["name"]) == ["At risk", "Deal seekers", "Loyal big spenders", "Regulars"]
    assert profile["size"].sum() == len(df)
    print("All checks passed")
