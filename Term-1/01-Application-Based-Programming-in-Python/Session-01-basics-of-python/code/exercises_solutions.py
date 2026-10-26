"""Session 01 practice solutions (inputs are hard-coded so the file runs on its own)."""

# 1
name, city, subject = "Bilal", "Karachi", "AI"
print(f"I am {name} from {city} and I love {subject}.")

# 2  (replace with float(input(...)) when practising)
length, width = 12.0, 10.5
print("Area =", length * width, "sq ft")

# 3
for ident in ["total", "2total", "total-marks", "_count", "for", "Name1"]:
    import keyword
    ok = ident.isidentifier() and not keyword.iskeyword(ident)
    print(f"{ident:12} -> {'valid' if ok else 'INVALID'}")

# 4
a, b = 5, 9
a, b = b, a
print(a, b)
assert (a, b) == (9, 5)
