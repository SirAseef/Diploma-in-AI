"""Session 06 - Practice exercise solutions."""
# notebook: run-in-code-dir
import io
import os
from pathlib import Path
import numpy as np
import pandas as pd

if __name__ == "__main__":
    out = Path("output"); out.mkdir(exist_ok=True)
    tsv = "roll\tname\tmarks\n1\tAli\t72\n2\tSana\tabsent\n3\tOmar\t65\n4\tZoya\tabsent\n"
    df = pd.read_csv(io.StringIO(tsv), sep="\t", na_values=["absent"])
    assert df["marks"].isna().sum() == 2

    p = out / "records.json"
    df.to_json(p, orient="records")
    assert pd.read_json(p, orient="records").equals(df)

    x = out / "two_sheets.xlsx"
    with pd.ExcelWriter(x) as xw:
        df.to_excel(xw, sheet_name="A", index=False)
        df.head(2).to_excel(xw, sheet_name="B", index=False)
    assert list(pd.read_excel(x, sheet_name=None).keys()) == ["A", "B"]

    rng = np.random.default_rng(0)
    big = pd.DataFrame({"id": range(20_000), "city": rng.choice(["Karachi", "Lahore"], 20_000),
                        "value": rng.normal(100, 15, 20_000)})
    big.to_csv(out / "big.csv", index=False); big.to_parquet(out / "big.parquet")
    ratio = os.path.getsize(out / "big.csv") / os.path.getsize(out / "big.parquet")
    print("CSV is", round(ratio, 1), "x bigger than Parquet")
    assert ratio > 1
    print("All exercise checks passed")
