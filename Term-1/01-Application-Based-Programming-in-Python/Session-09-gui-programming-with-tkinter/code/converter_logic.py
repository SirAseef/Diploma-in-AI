"""Pure conversion logic (no GUI) - easy to test."""
RATES = {"km -> miles": 0.621371, "kg -> pounds": 2.20462, "C -> F": None}


def convert(value, unit):
    if unit == "C -> F":
        return value * 9 / 5 + 32
    return value * RATES[unit]
