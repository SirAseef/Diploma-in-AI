"""Plain-Python illustration of a collection scan vs an index seek (what explain() reports as docs/keys examined)."""
from bisect import bisect_left, bisect_right


def collscan(docs, field, value):
    examined, hits = 0, []
    for d in docs:
        examined += 1
        if d.get(field) == value:
            hits.append(d)
    return {"stage": "COLLSCAN", "examined": examined, "returned": len(hits)}


def build_index(docs, field):
    """A sorted list of (key, position) pairs - a tiny stand-in for a B-tree."""
    return sorted((d.get(field), i) for i, d in enumerate(docs) if d.get(field) is not None)


def ixscan(index, value):
    keys = [k for k, _ in index]
    lo, comparisons, hi_bound = 0, 0, len(keys)
    left, right = 0, hi_bound
    while left < right:                      # binary search, counting comparisons
        mid = (left + right) // 2
        comparisons += 1
        if keys[mid] < value:
            left = mid + 1
        else:
            right = mid
    lo = left
    hi = bisect_right(keys, value, lo)
    return {"stage": "IXSCAN", "examined": comparisons + (hi - lo), "returned": hi - lo,
            "positions": [p for _, p in index[lo:hi]]}


if __name__ == "__main__":
    docs = [{"n": i} for i in range(1000)]
    assert collscan(docs, "n", 500)["examined"] == 1000
    r = ixscan(build_index(docs, "n"), 500)
    assert r["returned"] == 1 and r["examined"] <= 12
    print(r)
