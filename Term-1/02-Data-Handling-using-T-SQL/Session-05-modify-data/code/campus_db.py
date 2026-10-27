"""Sample 'campus' database used by every session of the T-SQL module.
SQL Server is not needed to practise: we build the same tables in SQLite (built into Python).
Run this file directly to see the row counts."""
import sqlite3

SCHEMA = """
CREATE TABLE faculty (
    faculty_id  INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL,
    subject     TEXT    NOT NULL,
    salary      INTEGER NOT NULL,
    hired_on    TEXT    NOT NULL
);
CREATE TABLE batches (
    batch_id    TEXT    PRIMARY KEY,
    course      TEXT    NOT NULL,
    faculty_id  INTEGER REFERENCES faculty(faculty_id),
    start_date  TEXT    NOT NULL,
    timing      TEXT
);
CREATE TABLE students (
    student_id  INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL,
    city        TEXT,
    batch_id    TEXT    REFERENCES batches(batch_id),
    email       TEXT,
    joined_on   TEXT    NOT NULL,
    fee_paid    INTEGER DEFAULT 0
);
CREATE TABLE marks (
    student_id  INTEGER REFERENCES students(student_id),
    subject     TEXT    NOT NULL,
    marks       INTEGER CHECK (marks BETWEEN 0 AND 100),
    PRIMARY KEY (student_id, subject)
);
"""

FACULTY = [
    (1, "Sana Iqbal", "Python", 180000, "2021-02-01"),
    (2, "Usman Tariq", "SQL", 165000, "2019-08-15"),
    (3, "Mehwish Raza", "Statistics", 172000, "2022-01-10"),
    (4, "Kamran Ali", "Web", 150000, "2023-06-01"),
    (5, "Nida Farooq", "AI", 210000, "2024-03-18"),
]
BATCHES = [
    ("AI-2601", "Diploma in AI", 1, "2026-01-12", "Morning"),
    ("AI-2602", "Diploma in AI", 2, "2026-04-06", "Evening"),
    ("DS-2601", "Data Science", 3, "2026-02-02", "Weekend"),
    ("WD-2601", "Web Development", 4, "2026-03-09", "Evening"),
    ("ML-2701", "Machine Learning", None, "2027-01-11", None),   # faculty not yet assigned
]
STUDENTS = [
    (101, "Ayesha Khan", "Karachi", "AI-2601", "ayesha@example.com", "2026-01-05", 45000),
    (102, "Bilal Ahmed", "Lahore", "AI-2601", None, "2026-01-07", 30000),
    (103, "Hira Siddiqui", "Karachi", "AI-2602", "hira@example.com", "2026-03-28", 45000),
    (104, "Omar Farooq", "Quetta", "DS-2601", "omar@example.com", "2026-01-25", 15000),
    (105, "Zara Hussain", "Karachi", "DS-2601", None, "2026-01-30", 45000),
    (106, "Hamza Malik", "Islamabad", "WD-2601", "hamza@example.com", "2026-03-01", 0),
    (107, "Fatima Noor", "Lahore", "AI-2602", "fatima@example.com", "2026-04-01", 45000),
    (108, "Ali Raza", None, "AI-2601", "ali@example.com", "2026-01-10", 30000),
    (109, "Mariam Javed", "Karachi", "WD-2601", None, "2026-03-05", 15000),
    (110, "Saad Qureshi", "Peshawar", None, "saad@example.com", "2026-10-20", 0),   # not placed in a batch yet
]
MARKS = [
    (101, "Python", 88), (101, "SQL", 79), (102, "Python", 64), (102, "SQL", 58),
    (103, "Python", 92), (103, "SQL", 95), (104, "Statistics", 71), (104, "Python", 49),
    (105, "Statistics", 83), (105, "Python", 77), (106, "Web", 68), (107, "Python", 74),
    (107, "SQL", 81), (108, "Python", 39), (108, "SQL", 45), (109, "Web", 90),
]


def connect(path=":memory:"):
    """Return a SQLite connection with the campus tables filled in."""
    # isolation_level=None = autocommit, like SQL Server: each statement commits unless you BEGIN a transaction
    con = sqlite3.connect(path, isolation_level=None)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(SCHEMA)
    con.executemany("INSERT INTO faculty VALUES (?,?,?,?,?)", FACULTY)
    con.executemany("INSERT INTO batches VALUES (?,?,?,?,?)", BATCHES)
    con.executemany("INSERT INTO students VALUES (?,?,?,?,?,?,?)", STUDENTS)
    con.executemany("INSERT INTO marks VALUES (?,?,?)", MARKS)
    con.commit()
    return con


def show(con, sql, params=()):
    """Run a query and print the result as a neat table; also return the rows."""
    cur = con.execute(sql, params)
    rows = cur.fetchall()
    if cur.description:
        cols = [d[0] for d in cur.description]
        widths = [max(len(str(c)), *(len(str(r[i])) for r in rows)) if rows else len(c) for i, c in enumerate(cols)]
        print(" | ".join(str(c).ljust(w) for c, w in zip(cols, widths)))
        print("-+-".join("-" * w for w in widths))
        for r in rows:
            print(" | ".join(str(v).ljust(w) for v, w in zip(r, widths)))
        print(f"({len(rows)} rows)\n")
    return rows


if __name__ == "__main__":
    con = connect()
    for t in ["faculty", "batches", "students", "marks"]:
        print(t, con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])
