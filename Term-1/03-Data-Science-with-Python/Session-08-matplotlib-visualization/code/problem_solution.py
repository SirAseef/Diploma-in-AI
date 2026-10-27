"""Session 08 - Real-life problem: one-page class results dashboard."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path


def make_class(n=120, seed=3):
    rng = np.random.default_rng(seed)
    section = rng.choice(list("ABCD"), n)
    attendance = rng.uniform(55, 100, n)
    boost = pd.Series(section).map({"A": 15, "B": 0, "C": -10, "D": 5}).to_numpy()
    total = (2.6 * attendance + boost + rng.normal(0, 25, n)).clip(0, 400)
    return pd.DataFrame({"section": section, "attendance": attendance.round(1), "total": total.round(0)})


def results_dashboard(df, path, pass_mark=200):
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), layout="constrained")
    ax = axes[0, 0]
    ax.hist(df["total"], bins=15, edgecolor="white")
    ax.axvline(pass_mark, color="red", ls="--", label="pass line"); ax.legend()
    ax.set(title="Distribution of total marks", xlabel="Total (out of 400)", ylabel="Students")
    avg = df.groupby("section")["total"].mean()
    bars = axes[0, 1].bar(avg.index, avg.values, color="#264653")
    axes[0, 1].bar_label(bars, fmt="%.0f"); axes[0, 1].set_title("Average by section")
    r = df["attendance"].corr(df["total"])
    for sec, g in df.groupby("section"):
        axes[1, 0].scatter(g["attendance"], g["total"], label=sec, alpha=0.7)
    axes[1, 0].set(title=f"Attendance vs marks (r = {r:.2f})", xlabel="Attendance %", ylabel="Total")
    axes[1, 0].legend(title="Section")
    axes[1, 1].boxplot([g["total"] for _, g in df.groupby("section")], tick_labels=avg.index)
    axes[1, 1].set_title("Spread by section")
    fig.suptitle("Class results dashboard (synthetic data)")
    fig.savefig(path, dpi=110); plt.close(fig)
    return {"pass_rate": round((df["total"] >= pass_mark).mean(), 3), "best_section": avg.idxmax(), "r": round(r, 2)}


if __name__ == "__main__":
    out = Path("output"); out.mkdir(exist_ok=True)
    df = make_class()
    summary = results_dashboard(df, out / "results_dashboard.png")
    print(summary)
    assert (out / "results_dashboard.png").stat().st_size > 10_000
    assert summary["best_section"] == "A"
    assert summary["r"] > 0.5
    print("All checks passed")
