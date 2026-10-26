"""Headless tests for the logic behind every Session 09 GUI. Run: python test_logic.py"""
from converter_logic import convert
from result_logic import bmi, check_login, compute_result, validate_marks

assert round(convert(10, "km -> miles"), 3) == 6.214
assert convert(100, "C -> F") == 212
assert validate_marks(["80", "70.5", "90"]) == [80.0, 70.5, 90.0]
for bad in (["abc", "1", "2"], ["120", "1", "2"]):
    try:
        validate_marks(bad)
        raise AssertionError("should have failed")
    except ValueError:
        pass
assert compute_result([80, 70, 90]) == (240, 80.0, "A")
assert compute_result([40, 50, 60]) == (150, 50.0, "C")
assert bmi(70, 1.75) == (22.9, "Normal")
assert check_login("student", "aptech123") and not check_login("student", "x")
print("All Session 09 logic tests passed.")
