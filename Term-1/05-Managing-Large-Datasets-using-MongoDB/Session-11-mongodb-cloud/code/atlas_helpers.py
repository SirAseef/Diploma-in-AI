"""Helpers for working safely with Atlas connection strings (no network needed)."""
import re
import time
from difflib import SequenceMatcher
from urllib.parse import parse_qs, quote_plus, urlsplit


def build_uri(user, password, host, db="", app="app", **options):
    opts = {"retryWrites": "true", "w": "majority", "appName": app, **options}
    query = "&".join(f"{k}={v}" for k, v in opts.items())
    return f"mongodb+srv://{quote_plus(user)}:{quote_plus(password)}@{host}/{db}?{query}"


def describe_uri(uri):
    parts = urlsplit(uri)
    return {"scheme": parts.scheme, "user": parts.username, "host": parts.hostname,
            "db": parts.path.lstrip("/"), "options": {k: v[0] for k, v in parse_qs(parts.query).items()}}


def mask(uri):
    return re.sub(r"(://[^:/@]+):[^@]+@", r"\1:****@", uri)


def connect_with_retry(factory, attempts=4, base_delay=0.5, sleep=time.sleep):
    for i in range(attempts):
        try:
            return factory()
        except ConnectionError:
            if i == attempts - 1:
                raise
            sleep(base_delay * 2 ** i)


def best_region(latency_ms):
    region = min(latency_ms, key=latency_ms.get)
    return region, latency_ms[region]


def fuzzy_search(docs, query, fields, threshold=0.8):
    """Rough idea of Atlas Search fuzzy matching: keep docs with a field value similar to the query."""
    hits = []
    for d in docs:
        values = []
        for f in fields:
            v = d.get(f, [])
            values += v if isinstance(v, list) else [v]
        best = max((SequenceMatcher(None, query.lower(), str(v).lower()).ratio() for v in values), default=0)
        if best >= threshold:
            hits.append((round(best, 2), d["name"]))
    return sorted(hits, reverse=True)


if __name__ == "__main__":
    u = build_uri("bot", "p@ss", "c0.x.mongodb.net", db="campus")
    assert describe_uri(u)["db"] == "campus" and "****" in mask(u)
    print(mask(u))
