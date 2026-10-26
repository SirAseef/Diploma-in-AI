"""Real-life problem: clean a messy marks CSV, log bad rows, write a report."""
import csv
from pathlib import Path

OUT = Path(__file__).parent / "output"


def grade(m):
    return "A" if m >= 80 else "B" if m >= 65 else "C" if m >= 50 else "F"


def clean_marks(src, dst, log):
    good, errors = [], []
    with open(src, encoding="utf-8") as f:
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            try:
                m = int(row["marks"])
                if not 0 <= m <= 100:
                    raise ValueError(f"marks {m} out of range")
                good.append({"name": row["name"].strip(), "marks": m, "grade": grade(m)})
            except (ValueError, TypeError) as e:
                errors.append(f"line {line_no}: {row} -> {e}")
    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["name", "marks", "grade"])
        w.writeheader()
        w.writerows(good)
    with open(log, "w", encoding="utf-8") as f:
        f.write("\n".join(errors))
    avg = sum(r["marks"] for r in good) / len(good)
    return len(good), len(errors), round(avg, 1)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    raw = OUT / "raw_marks.csv"
    raw.write_text("name,marks\nAli,72\nSana,91\nUmer,abc\nHira,58\nZaid,140\nNoor,84\n", encoding="utf-8")
    ok, bad, avg = clean_marks(raw, OUT / "report.csv", OUT / "errors.log")
    print(f"clean rows: {ok}, bad rows: {bad}, class average: {avg}")
    print((OUT / "errors.log").read_text())
    assert (ok, bad, avg) == (4, 2, 76.2)
