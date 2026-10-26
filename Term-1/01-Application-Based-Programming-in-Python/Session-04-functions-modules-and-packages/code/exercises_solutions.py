"""Session 04 practice solutions."""
from school.grades import attendance_status


def power(base, exp):
    return 1 if exp == 0 else base * power(base, exp - 1)


def reverse(text):
    return text if len(text) <= 1 else reverse(text[1:]) + text[0]


if __name__ == "__main__":
    print(power(2, 10), reverse("python"))
    words = sorted(["banana", "kiwi", "apple", "fig"], key=lambda w: len(w))
    print(words)
    print(attendance_status(80), attendance_status(60))
    assert power(2, 10) == 1024 and reverse("python") == "nohtyp"
    assert words[0] == "fig" and attendance_status(75) == "Allowed"
