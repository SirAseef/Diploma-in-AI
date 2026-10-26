"""Real-life problem: tiered electricity bill with tax."""

SLABS = [(100, 22), (100, 30), (float("inf"), 42)]  # (units in slab, Rs per unit)


def energy_charge(units):
    charge, remaining = 0, units
    for size, rate in SLABS:
        used = min(remaining, size)
        charge += used * rate
        remaining -= used
        if remaining <= 0:
            break
    return charge


def electricity_bill(units, tax_rate=0.17):
    base = energy_charge(units)
    return round(base * (1 + tax_rate), 2)


def print_summary(**houses):
    for house, units in houses.items():
        print(f"{house:8} {units:>4} units -> Rs {electricity_bill(units):,.2f}")


if __name__ == "__main__":
    print_summary(house_a=85, house_b=150, house_c=320)
    assert energy_charge(320) == 10240
    assert electricity_bill(320) == 11980.8
