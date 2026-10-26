"""Real-life problem: scrape the practice store, save CSV, answer price questions."""
import csv
from pathlib import Path
from bs4 import BeautifulSoup

HERE = Path(__file__).parent


def parse_price(text):
    return int(text.replace("Rs", "").replace(",", "").strip())


def scrape(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for card in soup.select("div.product"):
        rows.append({
            "title": card.select_one(".title").get_text(strip=True),
            "category": card["data-category"],
            "price": parse_price(card.select_one(".price").get_text()),
            "in_stock": "in" in card.select_one(".stock")["class"],
        })
    return rows


def analyse(rows):
    in_stock = [r for r in rows if r["in_stock"]]
    cheapest = min(in_stock, key=lambda r: r["price"])
    by_cat = {}
    for r in rows:
        by_cat.setdefault(r["category"], []).append(r["price"])
    priciest_cat = max(by_cat, key=lambda c: sum(by_cat[c]) / len(by_cat[c]))
    under_2000 = [r["title"] for r in rows if r["price"] < 2000]
    return cheapest, priciest_cat, under_2000


if __name__ == "__main__":
    rows = scrape((HERE / "sample_store.html").read_text(encoding="utf-8"))
    out = HERE / "output"
    out.mkdir(exist_ok=True)
    with open(out / "products.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    cheapest, cat, cheap = analyse(rows)
    print("Cheapest in stock:", cheapest["title"], cheapest["price"])
    print("Most expensive category on average:", cat)
    print("Under Rs 2,000:", cheap)
    assert cheapest["title"] == "USB Flash 64GB" and cat == "storage"
    assert cheap == ["Wireless Mouse", "USB Flash 64GB"]
