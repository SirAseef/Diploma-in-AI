"""Real-life problem: a tiny SQLite library manager with loans and overdue fines."""
import sqlite3
from datetime import date, timedelta

FINE_PER_DAY = 20


def setup(conn):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, title TEXT NOT NULL, available INTEGER DEFAULT 1);
    CREATE TABLE IF NOT EXISTS loans(id INTEGER PRIMARY KEY, book_id INTEGER REFERENCES books(id),
        member TEXT, due TEXT, returned INTEGER DEFAULT 0);""")


def add_book(conn, title):
    with conn:
        return conn.execute("INSERT INTO books(title) VALUES (?)", (title,)).lastrowid


def issue(conn, book_id, member, today, days=14):
    with conn:
        ok = conn.execute("SELECT available FROM books WHERE id = ?", (book_id,)).fetchone()
        if not ok or ok[0] == 0:
            return False
        conn.execute("UPDATE books SET available = 0 WHERE id = ?", (book_id,))
        conn.execute("INSERT INTO loans(book_id, member, due) VALUES (?, ?, ?)",
                     (book_id, member, (today + timedelta(days=days)).isoformat()))
    return True


def return_book(conn, book_id):
    with conn:
        conn.execute("UPDATE loans SET returned = 1 WHERE book_id = ? AND returned = 0", (book_id,))
        conn.execute("UPDATE books SET available = 1 WHERE id = ?", (book_id,))


def overdue(conn, today):
    rows = conn.execute("""SELECT b.title, l.member, l.due FROM loans l JOIN books b ON b.id = l.book_id
                           WHERE l.returned = 0 AND l.due < ? ORDER BY l.due""", (today.isoformat(),))
    return [(t, m, (today - date.fromisoformat(d)).days * FINE_PER_DAY) for t, m, d in rows]


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    setup(conn)
    py = add_book(conn, "Python Crash Course")
    ml = add_book(conn, "Hands-on ML")
    db = add_book(conn, "SQL Basics")
    start = date(2026, 10, 1)
    assert issue(conn, py, "Ali", start)
    assert not issue(conn, py, "Sana", start)          # already out
    assert issue(conn, ml, "Sana", start, days=7)
    assert issue(conn, db, "Hamza", start)
    return_book(conn, db)
    late = overdue(conn, date(2026, 10, 20))
    for title, member, fine in late:
        print(f"{title:22} {member:6} Rs {fine}")
    assert late == [("Hands-on ML", "Sana", 240), ("Python Crash Course", "Ali", 100)]
    print("all checks passed")
