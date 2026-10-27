"""Real-life problem: build a one-page sales dashboard for a small Karachi shop."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def make_sales(days=90, seed=1):
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2026-07-01", periods=days, freq="D")
    cats = rng.choice(["Clothing", "Shoes", "Accessories"], size=days * 4, p=[0.5, 0.3, 0.2])
    return pd.DataFrame({
        "date": np.repeat(dates, 4),
        "category": cats,
        "amount": rng.integers(500, 6000, size=days * 4),
    })


def build_dashboard(df, path):
    monthly = df.groupby(df["date"].dt.to_period("M"))["amount"].sum()
    by_cat = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    weekday = df.groupby(df["date"].dt.day_name())["amount"].mean()
    weekday = weekday.reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    daily = df.groupby("date")["amount"].sum()

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    axs[0, 0].plot(daily.index, daily.values, alpha=0.4, label="daily")
    axs[0, 0].plot(daily.index, daily.rolling(7).mean(), color="red", label="7-day average")
    axs[0, 0].set_title("Daily revenue"); axs[0, 0].legend(); axs[0, 0].tick_params(axis="x", rotation=30)
    b = axs[0, 1].bar(monthly.index.astype(str), monthly.values / 1000, color="teal")
    axs[0, 1].bar_label(b, fmt="%.0fk"); axs[0, 1].set_title("Revenue per month (thousand Rs)")
    axs[1, 0].pie(by_cat.values, labels=by_cat.index, autopct="%1.0f%%"); axs[1, 0].set_title("Share by category")
    axs[1, 1].barh(weekday.index, weekday.values, color="slateblue"); axs[1, 1].set_title("Average sale by weekday")
    fig.suptitle("Shop dashboard · Jul–Sep 2026", fontsize=15)
    fig.tight_layout(); fig.savefig(path, dpi=100); plt.close(fig)
    return {"best_category": by_cat.index[0], "best_weekday": weekday.idxmax(), "total": int(df["amount"].sum())}


if __name__ == "__main__":
    out = Path("output"); out.mkdir(exist_ok=True)
    sales = make_sales()
    info = build_dashboard(sales, out / "dashboard.png")
    print(info)
    assert (out / "dashboard.png").stat().st_size > 10_000
    assert info["best_category"] == "Clothing"   # 50% of orders are clothing
    print("dashboard OK")
