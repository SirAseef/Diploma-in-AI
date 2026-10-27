"""Session 10 practice solutions."""
import sqlite3


def make_products(conn):
    conn.execute("CREATE TABLE products(id INTEGER PRIMARY KEY, name TEXT, price REAL, qty INTEGER)")
    conn.executemany("INSERT INTO products(name, price, qty) VALUES (?, ?, ?)",
                     [("Pen", 30, 100), ("Notebook", 150, 40), ("Bag", 2200, 5),
                      ("Ruler", 60, 25), ("Marker", 90, 60)])
    conn.commit()


def stock_value(conn):
    return conn.execute("SELECT SUM(price * qty) FROM products").fetchone()[0]


def restock(conn, name, extra):
    with conn:
        cur = conn.execute("UPDATE products SET qty = qty + ? WHERE name = ?", (extra, name))
    return cur.rowcount == 1


def search(conn, text):
    rows = conn.execute("SELECT name FROM products WHERE LOWER(name) LIKE ?", (f"%{text.lower()}%",))
    return [r[0] for r in rows]


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    make_products(conn)
    print("stock value:", stock_value(conn))
    assert stock_value(conn) == 3000 + 6000 + 11000 + 1500 + 5400
    assert restock(conn, "Bag", 3) and not restock(conn, "Laptop", 1)
    assert search(conn, "MAR") == ["Marker"]
    print(search(conn, "e"))
    print("all checks passed")
