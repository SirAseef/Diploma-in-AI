"""Session 05 - Real-life problem: RFM segmentation for an online clothing store."""
# notebook: run-in-code-dir
import os
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from shop_data import feature_matrix, make_transactions, rfm_table


def name(row, overall):
    if row.R > 2 * overall.R:
        return "At risk"
    if row.disc > 0.5:
        return "Bargain hunters"
    if row.F >= overall.F * 1.5 and row.M >= overall.M * 1.5:
        return "Champions"
    return "Regulars"


def segment(tx):
    rfm = rfm_table(tx); X = feature_matrix(rfm)
    sil = {k: silhouette_score(X, KMeans(k, n_init=10, random_state=0).fit_predict(X)) for k in range(3, 7)}
    k = max(sil, key=sil.get)
    rfm["segment"] = KMeans(k, n_init=10, random_state=0).fit_predict(X)
    profile = rfm.groupby("segment")[["R", "F", "M", "disc"]].median()
    names = profile.apply(name, axis=1, overall=rfm[["R", "F", "M", "disc"]].median())
    rfm["segment_name"] = rfm.segment.map(names)
    return k, rfm, profile.assign(name=names)


if __name__ == "__main__":
    k, rfm, profile = segment(make_transactions(n_customers=800, seed=12))
    print("k =", k); print(profile.round(2))
    summary = rfm.groupby("segment_name").agg(customers=("M", "size"), revenue=("M", "sum"))
    summary["revenue_share"] = (summary.revenue / summary.revenue.sum()).round(3)
    print(summary)
    os.makedirs("output", exist_ok=True)
    rfm[["segment_name"]].to_csv("output/segments.csv")
    assert {"At risk", "Bargain hunters", "Champions"} <= set(rfm.segment_name)
    assert summary.loc["Champions", "revenue_share"] > summary.loc["Champions", "customers"] / len(rfm)
    print("OK")
