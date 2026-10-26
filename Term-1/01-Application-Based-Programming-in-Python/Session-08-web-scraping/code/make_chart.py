"""Scrape the practice page and chart average price per category -> ../images/avg_price_by_category.png"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from problem_solution import scrape

rows = scrape(open("sample_store.html", encoding="utf-8").read())
cats = {}
for r in rows:
    cats.setdefault(r["category"], []).append(r["price"])
avg = {c: sum(v) / len(v) for c, v in cats.items()}
order = sorted(avg, key=avg.get)
fig, ax = plt.subplots(figsize=(6.5, 3.6))
bars = ax.bar(order, [avg[c] for c in order], color="#6a1b9a")
ax.bar_label(bars, labels=[f"Rs {avg[c]:,.0f}" for c in order])
ax.set_ylim(0, max(avg.values()) * 1.18)
ax.set_ylabel("average price (Rs)"); ax.set_title("Scraped data: average price by category")
fig.tight_layout(); fig.savefig("../images/avg_price_by_category.png", dpi=120)
print(avg)
