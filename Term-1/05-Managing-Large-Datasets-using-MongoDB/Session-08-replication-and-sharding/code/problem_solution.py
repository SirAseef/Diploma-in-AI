"""Session 08 - Real-life problem: availability and shard-key choice for a food-delivery app."""
import random
from datetime import datetime, timedelta
from cluster_sim import ReplicaSet, hashed_router, ranged_router, route_counts


def availability(members, failures):
    rs = ReplicaSet([f"db{i}" for i in range(1, members + 1)])
    out = []
    for name in failures:
        rs.fail(name); rs.elect()
        out.append(rs.can_write())
    return out


def busiest_share(keys, router):
    counts = route_counts(keys, router)
    return round(max(counts.values()) / len(keys), 3)


if __name__ == "__main__":
    three = availability(3, ["db1", "db2"])
    five = availability(5, ["db1", "db2"])
    print("3 members, after 1 and 2 failures can write:", three)
    print("5 members, after 1 and 2 failures can write:", five)
    assert three == [True, False] and five == [True, True]

    rng = random.Random(88)
    now = datetime(2026, 10, 27, 12)
    orders = [{"city": rng.choices(["Karachi", "Lahore", "Islamabad"], [60, 25, 15])[0],
               "created_at": (now + timedelta(seconds=i)).timestamp(),
               "customer_id": rng.randrange(2_000_000)} for i in range(60_000)]
    city_router = lambda c: {"Islamabad": 0, "Karachi": 1, "Lahore": 2}[c]          # ranged by name
    old_bounds = [(now - timedelta(days=400)).timestamp(), (now - timedelta(days=200)).timestamp()]
    shares = {
        "city (ranged)": busiest_share([o["city"] for o in orders], city_router),
        "created_at (ranged)": busiest_share([o["created_at"] for o in orders], ranged_router(old_bounds)),
        "customer_id (hashed)": busiest_share([o["customer_id"] for o in orders], hashed_router(3)),
    }
    for k, v in shares.items():
        print(f"{k:<22} busiest shard gets {100 * v:.1f}% of new writes")
    best = min(shares, key=shares.get)
    print("recommend:", best)
    assert best == "customer_id (hashed)" and shares["customer_id (hashed)"] < 0.36
    assert shares["created_at (ranged)"] == 1.0 and shares["city (ranged)"] > 0.55
    print("All checks passed")
