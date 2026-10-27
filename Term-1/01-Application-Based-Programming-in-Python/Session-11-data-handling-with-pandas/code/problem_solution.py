"""Real-life problem: clean a messy month of shop orders and report revenue."""
import pandas as pd


def sample_orders():
    return pd.DataFrame({
        "date": ["2026-10-05", "2026-10-05", "2026-10-06", "2026-10-07", "2026-10-10",
                 "2026-10-11", "2026-10-12", "2026-10-12", "2026-10-17", "2026-10-18"],
        "product": ["Kurta", "Kurta", "Sneakers", "Cap", "Sneakers", "Kurta", "Watch", "Cap", "Watch", "Socks"],
        "category": ["Clothing", "Clothing", "Shoes", "Accessories", "Shoes",
                     "Clothing", "Accessories", "Accessories", "Accessories", "Clothing"],
        "price": ["Rs 2,500", "Rs 2,500", "Rs 6,000", "Rs 800", "6000",
                  "Rs 2,500", "Rs 9,500", "Rs 800", "n/a", "Rs 300"],
        "qty": [2, 2, 1, None, 1, 1, 1, 3, 1, 5],
    })


def clean_orders(raw):
    df = raw.drop_duplicates().copy()
    df["price"] = pd.to_numeric(df["price"].str.replace(r"[^0-9.]", "", regex=True), errors="coerce")
    df["qty"] = df["qty"].fillna(1).astype(int)
    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna(subset=["price"])
    df["revenue"] = df["price"] * df["qty"]
    return df


def report(df):
    by_cat = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
    top3 = df.groupby("product")["revenue"].sum().nlargest(3)
    best_day = df.groupby(df["date"].dt.day_name())["revenue"].sum().idxmax()
    return by_cat, top3, best_day


if __name__ == "__main__":
    df = clean_orders(sample_orders())
    by_cat, top3, best_day = report(df)
    print(df[["date", "product", "price", "qty", "revenue"]])
    print("\nRevenue by category:\n", by_cat)
    print("\nTop 3 products:\n", top3)
    print("\nBest day:", best_day)
    assert len(df) == 8                       # 1 duplicate and 1 unparseable price removed
    assert by_cat.index[0] == "Accessories" and by_cat.iloc[0] == 12700
    assert top3.index.tolist() == ["Sneakers", "Watch", "Kurta"]
    assert best_day == "Monday"
    print("all checks passed")
