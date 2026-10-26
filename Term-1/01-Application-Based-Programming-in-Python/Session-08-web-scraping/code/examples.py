"""Session 08 - Web Scraping: worked examples (offline on sample_store.html).
Run `python examples.py --live` to also try the live practice site books.toscrape.com."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - parse and find

# %%
import sys
from bs4 import BeautifulSoup

html = open("sample_store.html", encoding="utf-8").read()
soup = BeautifulSoup(html, "html.parser")
print(soup.title.get_text())
print(soup.find("h1").get_text(strip=True))
print(len(soup.find_all("div", class_="product")), "products")

# %% [markdown]
# ## Example 2 - extract every product

# %%
products = []
for card in soup.select("div.product"):
    products.append({
        "title": card.select_one(".title").get_text(strip=True),
        "price": int(card.select_one(".price").get_text().replace("Rs", "").replace(",", "")),
        "in_stock": "in" in card.select_one(".stock")["class"],
        "category": card["data-category"],
    })
for p in products[:3]:
    print(p)

# %% [markdown]
# ## Into pandas and CSV

# %%
import pandas as pd
df = pd.DataFrame(products)
print(df.groupby("category")["price"].mean().round(0))

# %% [markdown]
# ## Example 4 - robots.txt rules

# %%
from urllib import robotparser
rp = robotparser.RobotFileParser()
rp.parse(["User-agent: *", "Disallow: /admin/"])
print(rp.can_fetch("*", "https://example.com/admin/"), rp.can_fetch("*", "https://example.com/products"))

# %% [markdown]
# ## Example 3 - live, polite download (optional)
# Set `LIVE = True` in the notebook, or run the script with `--live`.

# %%
LIVE = "--live" in sys.argv
if LIVE:
    import time
    import requests
    HEADERS = {"User-Agent": "DiplomaAI-student-scraper/1.0 (learning project)"}
    r = requests.get("https://books.toscrape.com/", headers=HEADERS, timeout=10)
    r.raise_for_status()
    r.encoding = r.apparent_encoding  # fixes symbols like £ showing as Â£
    live = BeautifulSoup(r.text, "html.parser")
    for book in live.select("article.product_pod")[:5]:
        print(book.h3.a["title"], "|", book.select_one(".price_color").get_text())
    time.sleep(1)
else:
    print("Live demo skipped (offline mode).")
