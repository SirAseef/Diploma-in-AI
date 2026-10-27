"""Session 03 - Real-life problem: mobile shop sales report."""
import pandas as pd


def shop_report(sales):
    df = pd.DataFrame(sales)
    df["revenue"] = df["qty"] * df["unit_price"]
    top3 = df.nlargest(3, "revenue")
    per_brand = df.groupby("brand")["qty"].sum().sort_values(ascending=False)
    avg_price = df.groupby("item")["unit_price"].transform("mean")
    df["overcharged"] = df["unit_price"] > 1.2 * avg_price
    return df, top3, per_brand


if __name__ == "__main__":
    sales = [
        {"item": "charger", "brand": "Anker", "qty": 3, "unit_price": 1800},
        {"item": "charger", "brand": "Local", "qty": 10, "unit_price": 450},
        {"item": "earbuds", "brand": "Audionic", "qty": 2, "unit_price": 3500},
        {"item": "earbuds", "brand": "Audionic", "qty": 1, "unit_price": 5600},
        {"item": "cover", "brand": "Local", "qty": 15, "unit_price": 300},
        {"item": "earbuds", "brand": "Audionic", "qty": 1, "unit_price": 3400},
        {"item": "cable", "brand": "Anker", "qty": 4, "unit_price": 900},
    ]
    df, top3, per_brand = shop_report(sales)
    print(df, top3, per_brand, sep="\n\n")
    assert list(top3["revenue"]) == [7000, 5600, 5400]
    assert per_brand.index[0] == "Local" and per_brand["Local"] == 25
    assert df["overcharged"].sum() == 2   # Anker charger and the Rs 5600 earbuds
    print("All checks passed")
