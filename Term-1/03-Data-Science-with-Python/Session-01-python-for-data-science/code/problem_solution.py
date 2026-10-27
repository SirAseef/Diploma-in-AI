"""Session 01 - Real-life problem: attendance summary from raw text lines."""
from collections import defaultdict


def attendance_summary(lines, threshold=75):
    present, total = defaultdict(int), defaultdict(int)
    for line in lines:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 3 or not parts[1]:
            continue
        _, name, status = parts
        name = name.title()
        total[name] += 1
        present[name] += status.lower() == "present"
    report = {n: (present[n], total[n], round(100 * present[n] / total[n], 1)) for n in total}
    low = sorted(n for n, (_, _, pct) in report.items() if pct < threshold)
    return report, low


if __name__ == "__main__":
    lines = [
        "2026-10-05,Ali,present", "2026-10-05, sana ,PRESENT", "2026-10-05,Bilal,absent",
        "2026-10-06,ali,present", "2026-10-06,Sana,present", "2026-10-06,Bilal,absent",
        "", "broken line",
        "2026-10-07,Ali,absent", "2026-10-07,Sana,present", "2026-10-07,Bilal,present",
        "2026-10-08,Ali,present", "2026-10-08,Sana,present", "2026-10-08,Bilal,present",
    ]
    report, low = attendance_summary(lines)
    for name, (p, t, pct) in sorted(report.items()):
        print(f"{name:<6} {p}/{t}  {pct}%")
    print("Below 75%:", low)
    assert report["Ali"] == (3, 4, 75.0)
    assert report["Sana"] == (4, 4, 100.0)
    assert low == ["Bilal"]
    print("All checks passed")
