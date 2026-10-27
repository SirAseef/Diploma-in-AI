"""Session 08 - Practice exercise solutions."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    out = Path("output"); out.mkdir(exist_ok=True)
    months = range(1, 13)
    khi = [19, 21, 25, 28, 30, 31, 30, 29, 29, 28, 24, 20]
    lhr = [13, 16, 21, 27, 32, 34, 32, 31, 30, 26, 19, 14]
    fig, ax = plt.subplots()
    ax.plot(months, khi, label="Karachi"); ax.plot(months, lhr, label="Lahore"); ax.legend()
    assert len(ax.get_lines()) == 2
    plt.close(fig)

    sales = pd.Series({"Tea": 340, "Rusk": 120, "Biscuits": 260, "Milk": 410, "Bread": 180})
    fig, ax = plt.subplots()
    s = sales.sort_values(); ax.barh(s.index, s.values)
    assert [t.get_text() for t in ax.get_yticklabels()][-1] == "Milk"
    plt.close(fig)

    data = np.random.default_rng(1).normal(50, 10, 300)
    fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3.5))
    a.hist(data, bins=20); b.boxplot(data, orientation="horizontal")
    fig.savefig(out / "c.png", dpi=150); fig.savefig(out / "c.svg")
    plt.close(fig)
    assert (out / "c.png").exists() and (out / "c.svg").exists()
    print("All exercise checks passed")
