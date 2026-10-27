"""Session 09 - Practice exercise solutions."""
# notebook: run-in-code-dir
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from students_data import make_students

if __name__ == "__main__":
    df = make_students()
    order = df["programme"].value_counts().index
    ax = sns.countplot(data=df, x="programme", order=order)
    assert [t.get_text() for t in ax.get_xticklabels()][0] == order[0]
    plt.close("all")

    ax = sns.kdeplot(data=df, x="score", hue="campus", common_norm=False)
    assert len(ax.get_lines()) + len(ax.collections) >= 3
    plt.close("all")

    wide = pd.DataFrame({"month": [1, 2, 3], "Clifton": [10, 12, 15], "Gulshan": [8, 9, 13]})
    long = wide.melt(id_vars="month", var_name="branch", value_name="sales")
    assert long.shape == (6, 3)
    sns.lineplot(data=long, x="month", y="sales", hue="branch")
    plt.close("all")

    pt = df.pivot_table(index="campus", columns="programme", values="score", aggfunc="mean")
    ax = sns.heatmap(pt, annot=True, fmt=".0f", cmap="YlGnBu")
    assert pt.shape == (3, 4)
    plt.close("all")
    print("All exercise checks passed")
