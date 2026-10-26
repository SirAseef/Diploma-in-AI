"""Session 03 practice solutions."""


def is_even(n):
    return n % 2 == 0


def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32


def describe(*items):
    return f"{len(items)} items: {', '.join(items)}"


def make_email(first, last, domain="aptech.edu.pk"):
    return f"{first}.{last}@{domain}".lower()


if __name__ == "__main__":
    print(is_even(4), is_even(7))
    for c in range(0, 41, 10):
        print(c, "C =", celsius_to_fahrenheit(c), "F")
    print(describe("pen", "book", "bag"))
    print(make_email("Sara", "Khan"))
    assert is_even(10) and not is_even(3)
    assert celsius_to_fahrenheit(100) == 212
    assert describe("pen", "book", "bag") == "3 items: pen, book, bag"
    assert make_email("Sara", "Khan") == "sara.khan@aptech.edu.pk"
