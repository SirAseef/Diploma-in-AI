"""Synthetic online-shop transactions for Session 05 (original code)."""
import numpy as np
import pandas as pd

TODAY = pd.Timestamp("2026-10-27")
PERSONAS = {  # share, orders per year, avg amount, recency scale (days), discount share
    "champion": (0.15, 30, 6000, 10, 0.15),
    "regular": (0.40, 8, 3500, 40, 0.20),
    "bargain": (0.25, 6, 2000, 50, 0.80),
    "at_risk": (0.20, 4, 3000, 250, 0.20),
}


def make_transactions(n_customers=600, seed=5):
    rng = np.random.default_rng(seed)
    rows, oid = [], 0
    names = list(PERSONAS)
    probs = [PERSONAS[p][0] for p in names]
    for c in range(n_customers):
        persona = rng.choice(names, p=probs)
        _, freq, amt, rec, disc = PERSONAS[persona]
        n = max(1, rng.poisson(freq))
        last = TODAY - pd.Timedelta(days=int(rng.exponential(rec)))
        for _ in range(n):
            oid += 1
            date = last - pd.Timedelta(days=int(rng.uniform(0, 330)))
            if _ == 0:
                date = last
            rows.append((f"C{c:04d}", oid, date, round(rng.lognormal(np.log(amt), 0.4)), rng.random() < disc, persona))
    return pd.DataFrame(rows, columns=["customer", "order_id", "date", "amount", "discounted", "persona"])


def rfm_table(tx):
    rfm = tx.groupby("customer").agg(last=("date", "max"), F=("order_id", "nunique"),
                                     M=("amount", "sum"), disc=("discounted", "mean"),
                                     persona=("persona", "first"))
    rfm["R"] = (TODAY - rfm["last"]).dt.days
    return rfm.drop(columns="last")


def feature_matrix(rfm):
    from sklearn.preprocessing import StandardScaler
    return StandardScaler().fit_transform(np.column_stack([rfm.R, np.log1p(rfm.F), np.log1p(rfm.M), rfm.disc]))
