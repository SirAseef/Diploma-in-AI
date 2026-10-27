"""Session 01 - Real-life problem: describe electricity bills by area."""
import numpy as np
import pandas as pd


def describe_bills(df):
    g = df.groupby("area")["bill"]
    summary = pd.DataFrame({
        "n": g.size(), "mean": g.mean(), "median": g.median(), "sd": g.std(),
        "iqr": g.quantile(0.75) - g.quantile(0.25), "p90": g.quantile(0.9), "skew": g.skew(),
    })
    summary["cv"] = summary["sd"] / summary["mean"]
    z = (df["bill"] - g.transform("mean")) / g.transform("std")
    flagged = df[z.abs() > 3]
    more_variable = summary["cv"].idxmax()
    edges = list(range(0, int(df["bill"].max()) + 2000, 2000))
    freq = pd.cut(df["bill"], edges, right=False).value_counts().sort_index()
    table = pd.DataFrame({"count": freq, "pct": (100 * freq / freq.sum()).round(1)})
    table["cum_pct"] = table["pct"].cumsum()
    return summary.round(2), flagged, more_variable, table


if __name__ == "__main__":
    rng = np.random.default_rng(2)
    df = pd.concat([
        pd.DataFrame({"area": "Gulshan", "bill": rng.normal(9000, 1500, 400).round(0)}),
        pd.DataFrame({"area": "Korangi", "bill": rng.gamma(2.5, 1800, 400).round(0)}),
    ], ignore_index=True)
    df.loc[5, "bill"] = 25_000                       # one suspicious Gulshan bill
    summary, flagged, more_variable, table = describe_bills(df)
    print(summary, "\nflagged:\n", flagged, "\nmore variable:", more_variable)
    print(table.head(8))
    assert more_variable == "Korangi"
    assert 5 in flagged.index
    assert summary.loc["Korangi", "skew"] > 0.5 and summary.loc["Korangi", "mean"] > summary.loc["Korangi", "median"]
    assert table["count"].sum() == len(df)
    print("All checks passed")
