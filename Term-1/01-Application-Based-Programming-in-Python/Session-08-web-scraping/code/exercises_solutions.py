"""Session 08 practice solutions."""
import time
from pathlib import Path
from bs4 import BeautifulSoup

soup = BeautifulSoup((Path(__file__).parent / "sample_store.html").read_text(encoding="utf-8"), "html.parser")

# 1 links
for a in soup.find_all("a"):
    print(a.get_text(strip=True), "->", a.get("href"))

# 2 out of stock
out = len(soup.select("span.stock.out"))
print("Out of stock:", out)
assert out == 2

# 3 quotes
QUOTES_HTML = """
<div class="quote"><span class="text">"Simple is better than complex."</span><small class="author">Tim Peters</small></div>
<div class="quote"><span class="text">"Data beats opinions."</span><small class="author">Anonymous</small></div>
"""


def scrape_quotes(html):
    s = BeautifulSoup(html, "html.parser")
    return [(q.select_one(".text").get_text(strip=True), q.select_one(".author").get_text(strip=True))
            for q in s.select("div.quote")]


quotes = scrape_quotes(QUOTES_HTML)
print(quotes)
assert quotes[0][1] == "Tim Peters"


# 4 polite downloader (get is injectable so we can test without internet)
def download_all(urls, delay=1.0, get=None):
    if get is None:
        import requests
        get = requests.get
    pages = []
    for u in urls:
        pages.append(get(u, timeout=10).text)
        time.sleep(delay)
    return pages


class FakeResponse:
    def __init__(self, url):
        self.text = f"<html>{url}</html>"


pages = download_all(["a", "b"], delay=0.1, get=lambda u, timeout: FakeResponse(u))
assert pages == ["<html>a</html>", "<html>b</html>"]
print("download_all works")
