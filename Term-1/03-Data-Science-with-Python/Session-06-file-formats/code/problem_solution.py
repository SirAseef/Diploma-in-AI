"""Session 06 - Real-life problem: combine pharmacy branch files in three formats."""
# notebook: run-in-code-dir
import json
from pathlib import Path
import pandas as pd

COLS = ["date", "branch", "product", "qty", "price"]


def combine_branches(csv_path, xlsx_path, json_path):
    a = pd.read_csv(csv_path, sep=";", parse_dates=["date"], dayfirst=True)
    a["branch"] = "Clifton"
    b = pd.read_excel(xlsx_path).rename(columns={"Date": "date", "Product": "product", "Qty": "qty", "Price": "price"})
    b["date"] = pd.to_datetime(b["date"]); b["branch"] = "Gulshan"
    with open(json_path, encoding="utf-8") as f:
        c = pd.json_normalize(json.load(f))
    c = c.rename(columns={"item.name": "product", "item.price": "price", "sold": "qty", "on": "date"})
    c["date"] = pd.to_datetime(c["date"]); c["branch"] = "Saddar"
    allsales = pd.concat([a[COLS], b[COLS], c[COLS]], ignore_index=True)
    allsales["revenue"] = allsales["qty"] * allsales["price"]
    return allsales, allsales.groupby("branch")["revenue"].sum()


if __name__ == "__main__":
    out = Path("output"); out.mkdir(exist_ok=True)
    (out / "clifton.csv").write_text("date;product;qty;price\n03/10/2026;Panadol;10;35\n04/10/2026;ORS;5;60\n")
    pd.DataFrame({"Date": ["2026-10-03", "2026-10-05"], "Product": ["Brufen", "Panadol"],
                  "Qty": [4, 8], "Price": [90, 35]}).to_excel(out / "gulshan.xlsx", index=False)
    (out / "saddar.json").write_text(json.dumps([
        {"on": "2026-10-04", "sold": 12, "item": {"name": "ORS", "price": 60}},
        {"on": "2026-10-06", "sold": 2, "item": {"name": "Insulin pen", "price": 2500}}]))
    allsales, per_branch = combine_branches(out / "clifton.csv", out / "gulshan.xlsx", out / "saddar.json")
    allsales.to_parquet(out / "all_branches.parquet")
    print(allsales, per_branch, sep="\n\n")
    assert list(allsales.columns) == COLS + ["revenue"] and len(allsales) == 6
    assert per_branch.to_dict() == {"Clifton": 650, "Gulshan": 640, "Saddar": 5720}
    assert allsales["date"].dt.month.eq(10).all()
    print("All checks passed")
