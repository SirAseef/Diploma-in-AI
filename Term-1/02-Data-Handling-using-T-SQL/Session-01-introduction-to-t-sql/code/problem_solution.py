"""Real-life problem: set up a small library database for the campus and answer first questions."""
# notebook: run-in-code-dir
import sqlite3
from campus_db import show

LIBRARY = """
CREATE TABLE books (
    isbn        TEXT    PRIMARY KEY,
    title       TEXT    NOT NULL,
    author      TEXT    NOT NULL,
    category    TEXT    NOT NULL,
    copies      INTEGER NOT NULL CHECK (copies >= 0),
    added_on    TEXT    NOT NULL DEFAULT (date('now'))
);
"""
BOOKS = [
    ("978-1", "Python Crash Course", "E. Matthes", "Programming", 4),
    ("978-2", "Learning SQL", "A. Beaulieu", "Databases", 3),
    ("978-3", "Hands-On Machine Learning", "A. Geron", "AI", 2),
    ("978-4", "Naked Statistics", "C. Wheelan", "Statistics", 0),
    ("978-5", "Fluent Python", "L. Ramalho", "Programming", 1),
]


def build():
    con = sqlite3.connect(":memory:")
    con.executescript(LIBRARY)
    con.executemany("INSERT INTO books (isbn, title, author, category, copies) VALUES (?,?,?,?,?)", BOOKS)
    return con


def answers(con):
    available = show(con, "SELECT title, copies FROM books WHERE copies > 0 ORDER BY copies DESC")
    programming = show(con, "SELECT title FROM books WHERE category = 'Programming'")
    total = show(con, "SELECT SUM(copies) AS total_copies FROM books")[0][0]
    return available, programming, total


if __name__ == "__main__":
    con = build()
    available, programming, total = answers(con)
    assert len(available) == 4 and available[0][0] == "Python Crash Course"
    assert len(programming) == 2 and total == 10
    try:
        con.execute("INSERT INTO books (isbn, title, author, category, copies) VALUES ('978-1','x','y','z',1)")
    except sqlite3.IntegrityError as e:
        print("duplicate ISBN rejected:", e)
    print("library ready")
