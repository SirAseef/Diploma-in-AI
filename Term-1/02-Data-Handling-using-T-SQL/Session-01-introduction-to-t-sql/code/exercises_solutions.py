"""Session 01 - practice exercise solutions (SQLite). T-SQL versions are in the README."""
# notebook: run-in-code-dir
import sqlite3
from campus_db import connect, show

con = connect()

# 1. Show every faculty member's name and subject
ex1 = show(con, "SELECT name, subject FROM faculty")

# 2. Create a 'rooms' table: room_no (primary key), capacity (> 0), has_projector (0/1, default 1)
con.execute("""CREATE TABLE rooms (
    room_no       TEXT PRIMARY KEY,
    capacity      INTEGER NOT NULL CHECK (capacity > 0),
    has_projector INTEGER NOT NULL DEFAULT 1 CHECK (has_projector IN (0, 1))
)""")

# 3. Insert three rooms, one without saying has_projector
con.execute("INSERT INTO rooms (room_no, capacity, has_projector) VALUES ('Lab-1', 30, 1), ('Lab-2', 25, 0)")
con.execute("INSERT INTO rooms (room_no, capacity) VALUES ('Hall', 120)")
ex3 = show(con, "SELECT * FROM rooms")

# 4. Students who paid nothing yet, with their joining date
ex4 = show(con, "SELECT name, joined_on FROM students WHERE fee_paid = 0")

if __name__ == "__main__":
    assert len(ex1) == 5
    assert ("Hall", 120, 1) in ex3
    assert {r[0] for r in ex4} == {"Hamza Malik", "Saad Qureshi"}
    try:
        con.execute("INSERT INTO rooms VALUES ('Lab-3', 0, 1)"); raise SystemExit("CHECK failed")
    except sqlite3.IntegrityError:
        pass
    print("all exercise checks passed")
