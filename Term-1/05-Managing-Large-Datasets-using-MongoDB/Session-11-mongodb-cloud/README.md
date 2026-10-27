# Session 11 · MongoDB Cloud

> **Module:** Managing Large Datasets using MongoDB · **Term 1** · ⏱️ ~2 hours
> **You will learn:** what **MongoDB Atlas** (MongoDB's managed cloud service) provides, how to create a free cluster, configure **network access** and **database users**, build and secure a `mongodb+srv://` connection string, choose a region and tier, and use Atlas features — backups, monitoring/alerts, Performance Advisor, **Atlas Search**, Charts and Triggers — plus the Atlas CLI.

---

## 1. Why a managed cloud database?

Running MongoDB yourself means buying servers, installing, patching, configuring replica sets, taking backups and watching disks at 3 a.m. **Atlas** does all of that as a service on AWS, Google Cloud or Azure: you pick a size and region, and get a ready replica set with backups, monitoring and security built in. A free **M0** cluster is enough for learning and small projects.

> 📒 **Analogy:** Running your own server is owning a generator in your house — you buy diesel, service it and fix it when it fails. Atlas is the electricity company — you pay for what you use and someone else maintains the plant.

```mermaid
flowchart LR
    DEV["Your laptop / app<br/>PyMongo · mongosh · Compass"] -->|"mongodb+srv:// TLS"| FW{IP access list}
    FW -->|allowed| CL[(Atlas cluster<br/>3-node replica set)]
    FW -->|blocked| X[connection refused]
    CL --> BK[automatic backups]
    CL --> MON[monitoring · alerts · Performance Advisor]
    CL --> SR[Atlas Search]
    CL --> CH[Charts · Triggers]
```

## 2. Reference tables

| Getting started (Atlas UI) | |
|---|---|
| 1 | Sign up at `cloud.mongodb.com`, create an **Organization** and a **Project** |
| 2 | **Create cluster** → choose the free M0 tier, a cloud provider and a nearby region (e.g. AWS Mumbai `ap-south-1` or Bahrain `me-south-1` for Pakistan) |
| 3 | **Database Access** → add a database user (username + strong password, role e.g. `readWrite` on one db) |
| 4 | **Network Access** → add your current IP (avoid `0.0.0.0/0` except for short tests) |
| 5 | **Connect** → copy the driver connection string and put it in an environment variable |
| 6 | Load data (Compass, `mongoimport`, `mongorestore`, or your app) |

| Tier | Typical use | Notes |
|---|---|---|
| M0 (free) | learning, prototypes | shared, 512 MB storage, limited operations |
| Flex / shared | small apps, low traffic | pay-as-you-go, still shared hardware |
| Dedicated (M10+) | production | dedicated resources, backups, scaling, private networking |

| Connection string part | Example | Meaning |
|---|---|---|
| scheme | `mongodb+srv://` | DNS SRV lookup finds all replica-set hosts |
| credentials | `report_bot:<password>@` | URL-encode special characters in the password |
| host | `cluster0.abcde.mongodb.net` | cluster address |
| path | `/campus` | default database |
| options | `?retryWrites=true&w=majority&appName=campus-portal` | driver options |

| Atlas feature | What it gives you |
|---|---|
| Backups | scheduled snapshots, point-in-time restore (dedicated tiers) |
| Monitoring & alerts | charts of operations, connections, CPU; email/Slack alerts |
| Performance Advisor | suggests indexes from slow queries |
| Atlas Search | full-text search with relevance, autocomplete, fuzzy matching (`$search` stage) |
| Atlas Vector Search | similarity search on embeddings for AI / RAG apps (`$vectorSearch`) |
| Charts | dashboards built directly on collections |
| Triggers | run functions on data changes or schedules |
| Atlas CLI | `atlas setup`, `atlas clusters create`, automation from scripts |

```javascript
// Atlas Search (after creating a search index named "default" on students)
db.students.aggregate([
  { $search: { index: "default", text: { query: "pyton", path: ["name", "skills"], fuzzy: { maxEdits: 1 } } } },
  { $limit: 5 }, { $project: { name: 1, skills: 1, score: { $meta: "searchScore" } } }
])
```

> 🧪 An Atlas cluster needs an account and internet, so the session code focuses on what runs anywhere: **building and validating** connection strings safely (password encoding, no secrets in code), reading the URI from an environment variable, retrying connections with back-off, and a small local "fuzzy search" to illustrate what Atlas Search does. Set `MONGO_URI` to your Atlas string and every script in this module runs against the cloud.

## 3. Worked examples

Full runnable code: [`code/examples.py`](./code/examples.py) · helpers: [`code/atlas_helpers.py`](./code/atlas_helpers.py) · notebook: [`notebook.ipynb`](./notebook.ipynb)

### Example 1 — build a connection string with an encoded password
```python
uri = build_uri("report_bot", "P@ss:w0rd/2026", "cluster0.abcde.mongodb.net", db="campus", app="campus-portal")
# mongodb+srv://report_bot:P%40ss%3Aw0rd%2F2026@cluster0.abcde.mongodb.net/campus?retryWrites=true&w=majority&appName=campus-portal
```

### Example 2 — inspect a URI and hide the password in logs
```python
info = describe_uri(uri); print(info["host"], info["options"]); print(mask(uri))
```

### Example 3 — never hard-code secrets
```python
uri = os.environ.get("MONGO_URI")          # set in your shell / .env file / CI secret
```

### Example 4 — connect with retry and back-off
```python
client = connect_with_retry(factory, attempts=4, base_delay=0.5)
```

### Example 5 — choose a region by latency
```python
best_region({"ap-south-1 (Mumbai)": 48, "me-south-1 (Bahrain)": 39, "eu-west-1 (Ireland)": 160})
```

### Example 6 — what Atlas Search adds: fuzzy matching
```python
fuzzy_search(students, "pyton", fields=["skills"])     # finds "python" despite the typo
```

## 4. Common mistakes

| Mistake | Fix |
|---|---|
| Allowing `0.0.0.0/0` permanently | Add specific IPs, or use VPC peering / private endpoints |
| Password with `@` or `:` breaks the URI | URL-encode it (`urllib.parse.quote_plus`) |
| Committing the connection string to GitHub | Environment variables / secret managers; rotate the password if leaked |
| Using the Atlas admin user in the app | Create a least-privilege database user per app |
| Choosing a far-away region | Pick the region closest to your users/app servers |

## 5. Real-life coding problem 🧮

**Problem:** A Karachi startup is moving its MongoDB to Atlas. Write a **pre-flight checker** `preflight(config)` that receives a dict of settings (`user`, `password`, `host`, `db`, `ip_access_list`, `user_roles`, `region_latency_ms`) and returns a list of problems and the final masked URI. Rules: host must end with `.mongodb.net`; password ≥ 12 characters with a digit and a symbol; access list must not contain `0.0.0.0/0`; the app user must not have `atlasAdmin`/`root`; pick the lowest-latency region and warn if it is above 120 ms.

<details>
<summary>💡 Full solution</summary>

```python
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
```
Full file with good and bad configs: [`code/problem_solution.py`](./code/problem_solution.py)
</details>

## 6. Practice exercises

1. Encode the password `Karachi#2026!` for a URI and decode it back.
2. Parse `mongodb+srv://u:p@cluster9.xyz.mongodb.net/shop?retryWrites=true&w=majority` and return the database name and options as a dict.
3. Write `mask(uri)` so the password is replaced with `****` (keep the username).
4. List the Atlas UI steps to let a teammate's laptop connect with read-only access to `campus`.

<details>
<summary>✅ Solutions</summary>

```python
enc = quote_plus("Karachi#2026!"); unquote_plus(enc) == "Karachi#2026!"

describe_uri(uri)["db"], describe_uri(uri)["options"]

re.sub(r"(://[^:/@]+):[^@]+@", r"\1:****@", uri)

# Database Access -> Add user (role: read on campus) · Network Access -> Add teammate's IP · share the URI securely
```
File: [`code/exercises_solutions.py`](./code/exercises_solutions.py)
</details>

## 7. Quiz

1. What does the `+srv` in `mongodb+srv://` do?
2. Which two security settings must be configured before you can connect to a new Atlas cluster?
3. Why must special characters in the password be URL-encoded?
4. Which Atlas feature suggests indexes for slow queries?
5. Which aggregation stage runs an Atlas Search query?

<details>
<summary>Answers</summary>

1. Uses a DNS SRV record to discover all hosts of the cluster (and TXT options), so the string stays short and survives host changes · 2. A database user (Database Access) and an IP access-list entry (Network Access) · 3. Characters like `@`, `:` and `/` have special meaning in URIs and would break parsing · 4. Performance Advisor · 5. `$search` (and `$vectorSearch` for vector similarity).
</details>

## 8. Summary

- Atlas is MongoDB as a managed service: clusters, backups, monitoring and security handled for you.
- Set up: project → cluster (tier + region) → database user → IP access → connection string.
- Keep URIs out of code, URL-encode passwords, and use least-privilege users.
- Atlas adds Search, Vector Search, Charts, Triggers and Performance Advisor on top of the database.

---
[⬅ Session 10](../Session-10-mongodb-tools/) · [Module home](../README.md) · [Session 12 ➡](../Session-12-pymongo-connectivity/)

<sub>Original teaching material by Aseef Ahmed · not official Aptech courseware · CC BY-NC 4.0 (text) / MIT (code)</sub>
