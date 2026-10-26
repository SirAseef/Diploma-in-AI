"""Grading helpers."""


def letter_grade(marks):
    if marks >= 80:
        return "A"
    if marks >= 65:
        return "B"
    if marks >= 50:
        return "C"
    return "F"


def gpa(marks_list):
    points = {"A": 4.0, "B": 3.0, "C": 2.0, "F": 0.0}
    return round(sum(points[letter_grade(m)] for m in marks_list) / len(marks_list), 2)


def attendance_status(percent):
    """Practice exercise 4."""
    return "Allowed" if percent >= 75 else "Short"


if __name__ == "__main__":
    print(letter_grade(91), gpa([91, 70, 40]))
