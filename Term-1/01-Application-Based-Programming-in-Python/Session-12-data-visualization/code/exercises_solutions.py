"""Session 12 - practice exercise solutions. Charts saved to code/output/."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT = Path("output"); OUT.mkdir(exist_ok=True)


# 1. Line chart of daily temperature for one week, max and min on the same axes
def temperature_chart(path=OUT / "ex1_temperature.png"):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    tmax = [34, 35, 33, 36, 38, 37, 35]
    tmin = [26, 27, 26, 28, 29, 28, 27]
    fig, ax = plt.subplots()
    ax.plot(days, tmax, "r-o", label="max")
    ax.plot(days, tmin, "b-o", label="min")
    ax.fill_between(days, tmin, tmax, alpha=0.15)
    ax.set_title("Karachi temperature (°C)"); ax.legend()
    fig.savefig(path); plt.close(fig)
    return path


# 2. Horizontal bar chart of the 5 most common words in a sentence
def top_words_chart(text, path=OUT / "ex2_words.png"):
    words = pd.Series(text.lower().replace(",", "").replace(".", "").split())
    top = words.value_counts().head(5).sort_values()
    fig, ax = plt.subplots()
    ax.barh(top.index, top.values, color="darkorange")
    ax.set_title("Top 5 words")
    fig.savefig(path); plt.close(fig)
    return top.to_dict()


# 3. Pie chart of a monthly budget, biggest slice pulled out
def budget_pie(budget, path=OUT / "ex3_budget.png"):
    labels, values = list(budget), list(budget.values())
    explode = [0.1 if v == max(values) else 0 for v in values]
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.0f%%", explode=explode, startangle=90)
    ax.set_title("Monthly budget")
    fig.savefig(path); plt.close(fig)
    return labels[values.index(max(values))]


# 4. Grouped bar chart: two sections' average per subject
def grouped_bars(path=OUT / "ex4_grouped.png"):
    subjects = ["Python", "SQL", "Stats"]
    sec_a, sec_b = [72, 65, 70], [68, 74, 62]
    x = np.arange(len(subjects)); w = 0.38
    fig, ax = plt.subplots()
    ax.bar(x - w / 2, sec_a, w, label="Section A")
    ax.bar(x + w / 2, sec_b, w, label="Section B")
    ax.set_xticks(x, subjects); ax.legend(); ax.set_title("Average marks")
    fig.savefig(path); plt.close(fig)
    return path


if __name__ == "__main__":
    print(temperature_chart().exists())
    top = top_words_chart("Data is the new oil. Clean data, good data, more data is the goal.")
    print(top); assert list(top)[-1] == "data"
    print(budget_pie({"Rent": 30000, "Food": 18000, "Transport": 7000, "Savings": 10000}))
    print(grouped_bars().exists())
    print("all exercise checks passed")
