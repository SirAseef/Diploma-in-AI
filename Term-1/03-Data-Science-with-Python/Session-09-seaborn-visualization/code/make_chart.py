"""Session 09 - generate README images with Seaborn."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from students_data import make_students
from problem_solution import make_trips, trips_report

sns.set_theme(style="whitegrid")
df = make_students()
fig, axes = plt.subplots(2, 2, figsize=(12, 8), layout="constrained")
sns.histplot(data=df, x="score", hue="campus", kde=True, element="step", ax=axes[0, 0])
axes[0, 0].set_title("histplot: score by campus")
sns.violinplot(data=df, x="campus", y="score", hue="gender", split=True, ax=axes[0, 1])
axes[0, 1].set_title("violinplot: campus × gender")
sns.regplot(data=df, x="study_hours", y="score", scatter_kws={"alpha": 0.4}, ax=axes[1, 0])
axes[1, 0].set_title("regplot: study hours vs score")
corr = df[["study_hours", "attendance", "sleep", "score"]].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=axes[1, 1])
axes[1, 1].set_title("heatmap: correlations")
fig.suptitle("Seaborn overview (synthetic student data)")
fig.savefig("../images/seaborn_overview.png", dpi=105)
plt.close(fig)
trips_report(make_trips(), "../images/trips_report.png")
print("charts written")
