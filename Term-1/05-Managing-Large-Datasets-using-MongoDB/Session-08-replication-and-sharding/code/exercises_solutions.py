"""Session 08 - Practice exercise solutions."""
from cluster_sim import ReplicaSet, hashed_router, ranged_router, route_counts, shards_for_query

if __name__ == "__main__":
    rs = ReplicaSet([f"db{i}" for i in range(1, 6)])
    rs.fail("db1"); rs.fail("db2"); rs.elect()
    assert rs.can_write() and rs.write({"ok": 1}, w="majority")["acknowledged_by"] == 3
    rs.fail("db3"); rs.elect()
    assert not rs.can_write()
    print("5 members tolerate 2 failures for majority writes")

    ranged = route_counts(range(9000), ranged_router([3000, 6000]))
    hashed = route_counts(range(9000), hashed_router(3))
    print("ranged:", ranged, "| hashed:", hashed)
    assert ranged == {0: 3000, 1: 3000, 2: 3000} and max(hashed.values()) < 3300

    assert len(shards_for_query({"customer_id": 7}, "customer_id")) == 1
    assert len(shards_for_query({"order_no": "ORD-1"}, "customer_id")) == 3
    assert len(shards_for_query({"customer_id": 7, "status": "pending"}, "customer_id")) == 1
    print('mongosh: sh.enableSharding("campus"); sh.shardCollection("campus.attendance", { student_id: "hashed" })')
    print("All exercise checks passed")
