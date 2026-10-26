"""Real-life problem: parse bank SMS alerts with named regex groups."""
import re

SMS = """PKR 2,500.00 debited from card ****4821 on 12-10-2026 at FOODPANDA.
PKR 15,000.00 credited to card ****4821 on 13-10-2026 Salary.
PKR 799.50 debited from card ****4821 on 14-10-2026 at DARAZ."""

PATTERN = re.compile(
    r"PKR\s(?P<amount>[\d,]+\.\d{2})\s(?P<kind>debited|credited)"
    r".*?\*{4}(?P<card>\d{4})\son\s(?P<date>\d{2}-\d{2}-\d{4})"
)


def parse_alerts(text):
    out = []
    for m in PATTERN.finditer(text):
        d = m.groupdict()
        d["amount"] = float(d["amount"].replace(",", ""))
        out.append(d)
    return out


if __name__ == "__main__":
    alerts = parse_alerts(SMS)
    for a in alerts:
        print(a)
    spent = sum(a["amount"] for a in alerts if a["kind"] == "debited")
    print("Total spent: PKR", spent)
    assert len(alerts) == 3 and spent == 3299.5
