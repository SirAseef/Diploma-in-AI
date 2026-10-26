"""Grade a class of 40 with if/elif and plot the grade counts -> ../images/grade_distribution.png"""
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

random.seed(7)
marks = [max(0, min(100, round(random.gauss(68, 13)))) for _ in range(40)]

counts = {"A": 0, "B": 0, "C": 0, "F": 0}
for m in marks:
    if m >= 80:
        counts["A"] += 1
    elif m >= 65:
        counts["B"] += 1
    elif m >= 50:
        counts["C"] += 1
    else:
        counts["F"] += 1

fig, ax = plt.subplots(figsize=(6, 3.6))
bars = ax.bar(counts.keys(), counts.values(), color=["#2e7d32", "#1565c0", "#f9a825", "#c62828"])
ax.bar_label(bars); ax.set_ylim(0, max(counts.values()) * 1.2)
ax.set_title("Grade distribution (40 students, if/elif grader)")
ax.set_xlabel("Grade"); ax.set_ylabel("Students")
fig.tight_layout()
fig.savefig("../images/grade_distribution.png", dpi=120)
print(counts)
