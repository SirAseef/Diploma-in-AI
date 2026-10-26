"""Pure logic for the Student Result Calculator (Session 09 problem) and exercises."""


def validate_marks(values):
    marks = []
    for v in values:
        m = float(v)
        if not 0 <= m <= 100:
            raise ValueError(f"{m} is not between 0 and 100")
        marks.append(m)
    return marks


def compute_result(marks):
    total = sum(marks)
    pct = round(total / (len(marks) * 100) * 100, 1)
    grade = "A" if pct >= 80 else "B" if pct >= 65 else "C" if pct >= 50 else "F"
    return total, pct, grade


def bmi(weight_kg, height_m):
    value = round(weight_kg / height_m ** 2, 1)
    if value < 18.5:
        cat = "Underweight"
    elif value < 25:
        cat = "Normal"
    elif value < 30:
        cat = "Overweight"
    else:
        cat = "Obese"
    return value, cat


USERS = {"student": "aptech123"}


def check_login(username, password):
    return USERS.get(username) == password
