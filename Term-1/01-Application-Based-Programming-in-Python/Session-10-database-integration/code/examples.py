"""Session 10 - Database Integration with Python: worked examples (SQLite, in memory)."""

# %% [markdown]
# ## Example 1 - connect and create a table

# %%
import sqlite3
conn = sqlite3.connect(":memory:")   # use "school.db" to keep a file on disk
cur = conn.cursor()
cur.execute("""CREATE TABLE students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city TEXT,
    marks INTEGER CHECK (marks BETWEEN 0 AND 100))""")
print("sqlite version:", sqlite3.sqlite_version)

# %% [markdown]
# ## Example 2 - insert one row and many rows

# %%
cur.execute("INSERT INTO students(name, city, marks) VALUES (?, ?, ?)", ("Ayesha", "Karachi", 88))
data = [("Bilal", "Lahore", 64), ("Hira", "Karachi", 92), ("Omar", "Quetta", 47)]
cur.executemany("INSERT INTO students(name, city, marks) VALUES (?, ?, ?)", data)
conn.commit()
print("last id:", cur.lastrowid)

# %% [markdown]
# ## Example 3 - read with filters, ordering and aggregates

# %%
for row in cur.execute("SELECT name, marks FROM students WHERE city = ? ORDER BY marks DESC", ("Karachi",)):
    print(row)
cur.execute("SELECT city, COUNT(*), ROUND(AVG(marks), 1) FROM students GROUP BY city ORDER BY city")
print(cur.fetchall())

# %% [markdown]
# ## Example 4 - update and delete

# %%
cur.execute("UPDATE students SET marks = marks + 5 WHERE marks < ?", (50,))
print(cur.rowcount, "row(s) updated")
cur.execute("DELETE FROM students WHERE name = ?", ("Bilal",))
conn.commit()
print(cur.execute("SELECT name, marks FROM students").fetchall())

# %% [markdown]
# ## Example 5 - transactions: all or nothing

# %%
try:
    with conn:
        cur.execute("INSERT INTO students(name, marks) VALUES (?, ?)", ("Zara", 70))
        cur.execute("INSERT INTO students(name, marks) VALUES (?, ?)", ("Bad", 140))
except sqlite3.IntegrityError as e:
    print("Rolled back:", e)
print("Zara saved?", cur.execute("SELECT COUNT(*) FROM students WHERE name='Zara'").fetchone()[0] == 1)

# %% [markdown]
# ## Example 6 - SQL injection demo and rows as dictionaries

# %%
evil = "x' OR '1'='1"
unsafe = cur.execute(f"SELECT COUNT(*) FROM students WHERE name = '{evil}'").fetchone()[0]
safe = cur.execute("SELECT COUNT(*) FROM students WHERE name = ?", (evil,)).fetchone()[0]
print("f-string query matched", unsafe, "rows; parameterised matched", safe)

conn.row_factory = sqlite3.Row
cur = conn.cursor()
for r in cur.execute("SELECT * FROM students"):
    print(dict(r))
conn.close()
