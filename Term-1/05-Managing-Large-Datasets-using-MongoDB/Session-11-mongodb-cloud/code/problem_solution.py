"""Session 11 - Real-life problem: Atlas migration pre-flight checker."""
# notebook: run-in-code-dir
import re
from atlas_helpers import best_region, build_uri, mask


def preflight(cfg):
    problems = []
    if not cfg["host"].endswith(".mongodb.net"):
        problems.append("host is not an Atlas hostname")
    pw = cfg["password"]
    if len(pw) < 12 or not re.search(r"\d", pw) or not re.search(r"[^\w]", pw):
        problems.append("weak password")
    if "0.0.0.0/0" in cfg["ip_access_list"]:
        problems.append("access list open to the whole internet")
    if set(cfg["user_roles"]) & {"atlasAdmin", "root"}:
        problems.append("app user has admin privileges")
    region, ms = best_region(cfg["region_latency_ms"])
    if ms > 120:
        problems.append(f"nearest region {region} is slow ({ms} ms)")
    uri = build_uri(cfg["user"], pw, cfg["host"], db=cfg["db"], app=cfg.get("app", "app"))
    return problems, region, mask(uri)


if __name__ == "__main__":
    good = {"user": "orders_app", "password": "Gul$han-2026-Secure", "host": "prod.k3xyz.mongodb.net", "db": "orders",
            "ip_access_list": ["203.0.113.10/32"], "user_roles": ["readWrite"],
            "region_latency_ms": {"ap-south-1": 47, "me-south-1": 38, "eu-central-1": 140}, "app": "orders-api"}
    bad = {**good, "password": "karachi123", "host": "192.168.1.20", "ip_access_list": ["0.0.0.0/0"],
           "user_roles": ["atlasAdmin"], "region_latency_ms": {"us-east-1": 230, "eu-west-1": 160}}
    p_good, region, uri = preflight(good)
    p_bad, region_bad, _ = preflight(bad)
    print("good config ->", p_good, region, uri)
    print("bad config  ->", p_bad)
    assert p_good == [] and region == "me-south-1" and "Gul" not in uri
    assert len(p_bad) == 5
    print("All checks passed")
