"""Real-life problem: 3-attempt PIN login with validation."""

CORRECT_PIN = "4826"


def login(attempts):
    """attempts: list of PINs the user types, in order."""
    for count, pin in enumerate(attempts, start=1):
        if len(pin) != 4 or not pin.isdigit():
            print(f"Attempt {count}: PIN must be 4 digits")
        elif pin == CORRECT_PIN:
            print(f"Attempt {count}: Welcome!")
            return True
        else:
            print(f"Attempt {count}: Wrong PIN")
        if count == 3:
            print("Account locked. Contact the bank.")
            return False
    return False


if __name__ == "__main__":
    assert login(["12a4", "1111", "4826"]) is True
    assert login(["0000", "1234", "9999"]) is False
