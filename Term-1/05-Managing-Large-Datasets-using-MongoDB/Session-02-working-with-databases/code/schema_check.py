"""A tiny plain-Python stand-in for MongoDB $jsonSchema validation (mongomock can't enforce validators)."""
import re

STUDENT_SCHEMA = {
    "required": ["name", "batch", "marks"],
    "types": {"name": str, "batch": str, "marks": dict, "phone": str},
    "min_length": {"name": 3},
    "enum": {"batch": ["DS-01", "DS-02", "AI-01"]},
    "range": {"marks.python": (0, 100), "marks.sql": (0, 100)},
    "pattern": {"phone": r"03\d{2}-\d{7}"},
}


def _get(doc, dotted):
    for part in dotted.split("."):
        if not isinstance(doc, dict) or part not in doc:
            return None
        doc = doc[part]
    return doc


def check(doc, schema):
    problems = [f"missing {f}" for f in schema.get("required", []) if f not in doc]
    for f, t in schema.get("types", {}).items():
        if f in doc and not isinstance(doc[f], t):
            problems.append(f"{f} must be {t.__name__}")
    for f, n in schema.get("min_length", {}).items():
        if isinstance(doc.get(f), str) and len(doc[f]) < n:
            problems.append(f"{f} too short")
    for f, allowed in schema.get("enum", {}).items():
        if f in doc and doc[f] not in allowed:
            problems.append(f"{f} not allowed")
    for f, (lo, hi) in schema.get("range", {}).items():
        v = _get(doc, f)
        if v is not None and not lo <= v <= hi:
            problems.append(f"{f} out of range")
    for f, pat in schema.get("pattern", {}).items():
        if isinstance(doc.get(f), str) and not re.fullmatch(pat, doc[f]):
            problems.append(f"{f} has wrong format")
    return problems


if __name__ == "__main__":
    assert check({"name": "Sana Khan", "batch": "DS-01", "marks": {"python": 90}}, STUDENT_SCHEMA) == []
    print(check({"name": "Al", "batch": "XX-9", "marks": {"python": 120}, "phone": "12345"}, STUDENT_SCHEMA))
