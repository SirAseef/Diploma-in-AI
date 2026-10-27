"""Session 04 - Real-life problem: food-delivery weekly, rider and area report."""
import numpy as np
import pandas as pd


def delivery_report(orders, riders):
    o = orders.copy()
    o["date"] = pd.to_datetime(o["date"])
    weekly = o.set_index("date")["amount"].resample("W").sum()
    per_rider = (o.groupby("rider_id")
                   .agg(orders=("order_id", "count"), total=("amount", "sum"), avg_min=("minutes", "mean"))
                   .reset_index()
                   .merge(riders, on="rider_id", how="left", validate="one_to_one")
                   .sort_values("avg_min"))
    o["weekday"] = o["date"].dt.day_name()
    pivot = pd.pivot_table(o, index="area", columns="weekday", values="order_id", aggfunc="count", fill_value=0)
    return weekly, per_rider, pivot


if __name__ == "__main__":
    rng = np.random.default_rng(11)
    n = 200
    riders = pd.DataFrame({"rider_id": [1, 2, 3, 4], "name": ["Kashif", "Naveed", "Zubair", "Imran"],
                           "bike": ["CD-70", "CG-125", "CD-70", "YBR"]})
    speed = {1: 28, 2: 35, 3: 22, 4: 31}
    rid = rng.choice([1, 2, 3, 4], n)
    orders = pd.DataFrame({
        "order_id": range(1, n + 1),
        "date": rng.choice(pd.date_range("2026-10-01", "2026-10-28"), n),
        "rider_id": rid,
        "area": rng.choice(["Gulshan", "Johar", "PECHS", "North Nazimabad"], n),
        "amount": rng.integers(500, 3000, n),
        "minutes": [speed[r] + rng.integers(-5, 6) for r in rid],
    })
    weekly, per_rider, pivot = delivery_report(orders, riders)
    print(weekly, per_rider, pivot, sep="\n\n")
    assert weekly.sum() == orders["amount"].sum()
    assert per_rider.iloc[0]["name"] == "Zubair"          # fastest average
    assert per_rider["orders"].sum() == n
    assert pivot.values.sum() == n
    print("All checks passed")
