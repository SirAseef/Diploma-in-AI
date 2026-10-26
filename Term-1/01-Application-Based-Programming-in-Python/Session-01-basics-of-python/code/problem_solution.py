"""Real-life problem: tea stall bill with 5% service charge."""

TEA_PRICE = 80
PARATHA_PRICE = 120
SERVICE_RATE = 0.05


def make_bill(cups, parathas):
    subtotal = cups * TEA_PRICE + parathas * PARATHA_PRICE
    service = subtotal * SERVICE_RATE
    total = subtotal + service
    lines = [
        "----- CHAI CORNER -----",
        f"Tea      x{cups:<3} Rs {cups * TEA_PRICE:>6}",
        f"Paratha  x{parathas:<3} Rs {parathas * PARATHA_PRICE:>6}",
        f"Service 5%     Rs {service:>6.0f}",
        f"TOTAL          Rs {total:>6.0f}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(make_bill(3, 2))
    assert "Rs    504" in make_bill(3, 2)  # (240 + 240) * 1.05 = 504
