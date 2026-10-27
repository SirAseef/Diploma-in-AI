"""A tiny, plain-Python simulation of replica-set elections/write concern and shard routing (teaching only)."""
import hashlib
from bisect import bisect_right
from collections import Counter


class ReplicaSet:
    def __init__(self, members):
        self.members = list(members)
        self.healthy = set(members)
        self.primary = members[0]
        self.log = []

    def majority(self):
        return len(self.members) // 2 + 1

    def fail(self, name):
        self.healthy.discard(name)
        if self.primary == name:
            self.primary = None

    def recover(self, name):
        self.healthy.add(name)

    def elect(self):
        if self.primary in self.healthy:
            return self.primary
        if len(self.healthy) >= self.majority():
            self.primary = sorted(self.healthy)[0]
        else:
            self.primary = None
        return self.primary

    def can_write(self):
        return self.primary is not None

    def write(self, doc, w=1):
        if not self.can_write():
            raise RuntimeError("no primary: replica set is read-only")
        needed = self.majority() if w == "majority" else int(w)
        if len(self.healthy) < needed:
            raise TimeoutError(f"write concern {w} not satisfied ({len(self.healthy)} healthy)")
        self.log.append(doc)
        return {"ok": 1, "acknowledged_by": needed}


def ranged_router(boundaries):
    """boundaries [b1, b2] -> shard 0: < b1, shard 1: b1..b2, shard 2: >= b2."""
    return lambda key: bisect_right(boundaries, key)


def hashed_router(n_shards):
    return lambda key: int(hashlib.md5(str(key).encode()).hexdigest(), 16) % n_shards


def route_counts(keys, router):
    return dict(sorted(Counter(router(k) for k in keys).items()))


def shards_for_query(query, key, n_shards=3, router=None):
    router = router or hashed_router(n_shards)
    return [router(query[key])] if key in query else list(range(n_shards))


def score_key(docs, field):
    counts = Counter(d[field] for d in docs)
    return {"field": field, "cardinality": len(counts), "max_share": round(max(counts.values()) / len(docs), 3)}


if __name__ == "__main__":
    rs = ReplicaSet(["db1", "db2", "db3"]); rs.fail("db1")
    assert rs.elect() == "db2"
    rs.fail("db2")
    assert rs.elect() is None
    print(route_counts(range(9000), hashed_router(3)))
