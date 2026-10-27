"""Session 02 - Real-life problem: street electricity report with NumPy (no loops)."""
import numpy as np


def street_report(usage, slab=200, low=22, high=35):
    monthly = usage.sum(axis=1) * 30
    peak_hour = int(usage.sum(axis=0).argmax())
    above = np.flatnonzero(monthly > monthly.mean())
    bill = np.where(monthly <= slab, monthly * low, slab * low + (monthly - slab) * high)
    return monthly, peak_hour, above, bill.round(0)


if __name__ == "__main__":
    rng = np.random.default_rng(1)
    hours = np.arange(24)
    profile = 0.2 + 0.6 * np.exp(-((hours - 20) ** 2) / 8)   # evening peak around 8 pm
    scale = np.array([0.6, 0.9, 1.5, 0.8, 1.2])[:, None]
    usage = profile * scale + rng.uniform(0, 0.05, (5, 24))
    monthly, peak, above, bill = street_report(usage)
    print("monthly kWh:", monthly.round(1))
    print("peak hour:", peak, "| above average:", above, "| bills Rs:", bill)
    assert usage.shape == (5, 24)
    assert peak == 20
    assert list(above) == [2, 4]
    # manual check of slab formula for the heaviest house
    m = monthly[2]
    assert bill[2] == round(200 * 22 + (m - 200) * 35)
    print("All checks passed")
