"""Session 07 - Real-life problem: clean scraped Karachi property listings."""
import re
import numpy as np
import pandas as pd

AREAS = {"dha": "DHA", "johar": "Gulistan-e-Johar", "gulshan": "Gulshan-e-Iqbal", "bahria": "Bahria Town"}


def parse_price(text):
    if pd.isna(text):
        return np.nan
    t = str(text).lower().replace(",", "")
    num = float(re.findall(r"[\d.]+", t)[0])
    if "crore" in t:
        return num * 1e7
    if "lac" in t or "lakh" in t:
        return num * 1e5
    return num


def clean_area(text):
    t = str(text).lower()
    return next((v for k, v in AREAS.items() if k in t), "Other")


def clean_listings(df):
    d = df.copy()
    d["area"] = d["area"].map(clean_area)
    d["size_sqft"] = pd.to_numeric(d["size_sqft"].astype(str).str.extract(r"([\d.]+)")[0], errors="coerce")
    d["price"] = d["price"].map(parse_price)
    d = d.drop_duplicates()
    d.loc[~d["size_sqft"].between(300, 5000), "size_sqft"] = np.nan
    d["size_sqft"] = d["size_sqft"].fillna(d.groupby("area")["size_sqft"].transform("median"))
    d["price_per_sqft"] = (d["price"] / d["size_sqft"]).round(0)
    return d.reset_index(drop=True)


if __name__ == "__main__":
    raw = pd.DataFrame({
        "area": ["DHA Phase 6", "dha", "Gulistan-e-Johar Block 15", "johar", "Gulshan Block 13", "DHA Phase 6", "Bahria Town Precinct 10"],
        "size_sqft": ["1200 sq ft", "1000", "950", None, "1100 sqft", "1200 sq ft", "40000"],
        "price": ["3.6 crore", "2.5 crore", "95 lac", "Rs 8,500,000", "1.32 crore", "3.6 crore", "1.1 crore"],
    })
    clean = clean_listings(raw)
    print(clean)
    assert len(clean) == 6                                     # one duplicate removed
    assert clean.loc[0, "price"] == 36_000_000 and clean.loc[2, "price"] == 9_500_000
    assert clean.loc[3, "size_sqft"] == 950                     # filled with Johar median
    assert np.isnan(clean.loc[5, "size_sqft"])                  # only Bahria listing had an impossible size
    assert clean.loc[0, "price_per_sqft"] == 30000
    print("All checks passed")
