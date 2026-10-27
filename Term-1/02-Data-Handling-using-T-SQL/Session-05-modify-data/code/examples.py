"""Session 05 - Modify Data Using T-SQL Statements: worked examples (SQLite; T-SQL in README).
RETURNING needs SQLite 3.35+ (bundled with recent Python)."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - INSERT: one row, several rows, and naming the columns

# %%
import sqlite3
from campus_db import connect, show
con = connect()
con.execute("INSERT INTO students (student_id, name, city, batch_id, joined_on) VALUES (111, 'Iqra Shah', 'Hyderabad', 'DS-2601', '2026-10-22')")
con.execute("""INSERT INTO students (student_id, name, city, batch_id, joined_on, fee_paid) VALUES
    (112, 'Taha Baig', 'Karachi', 'AI-2602', '2026-10-23', 15000),
    (113, 'Laiba Aslam', 'Sukkur', 'AI-2602', '2026-10-23', 45000)""")
show(con, "SELECT student_id, name, city, fee_paid FROM students WHERE student_id >= 111")   # fee_paid default 0

# %% [markdown]
# ## Example 2 - INSERT ... SELECT and creating a table from a query

# %%
con.execute("CREATE TABLE toppers (student_id INTEGER, subject TEXT, marks INTEGER)")
con.execute("INSERT INTO toppers SELECT student_id, subject, marks FROM marks WHERE marks >= 85")
show(con, "SELECT * FROM toppers")
con.execute("CREATE TABLE karachi_students AS SELECT student_id, name FROM students WHERE city = 'Karachi'")  # T-SQL: SELECT ... INTO
show(con, "SELECT COUNT(*) AS copied FROM karachi_students")

# %% [markdown]
# ## Example 3 - UPDATE: one row, many rows, computed values

# %%
con.execute("UPDATE students SET email = 'bilal@example.com' WHERE student_id = 102")
con.execute("UPDATE faculty SET salary = CAST(ROUND(salary * 1.10) AS INTEGER) WHERE hired_on < '2022-01-01'")      # 10% raise for seniors
show(con, "SELECT name, hired_on, salary FROM faculty")

# %% [markdown]
# ## Example 4 - UPDATE using another table (grace marks for one batch)

# %%
con.execute("""UPDATE marks SET marks = MIN(marks + 5, 100)
WHERE subject = 'Python'
  AND student_id IN (SELECT student_id FROM students WHERE batch_id = 'AI-2601')""")
show(con, "SELECT student_id, subject, marks FROM marks WHERE subject = 'Python' AND student_id IN (101, 102, 108)")

# %% [markdown]
# ## Example 5 - DELETE with RETURNING (T-SQL: OUTPUT deleted.*)

# %%
gone = con.execute("DELETE FROM toppers WHERE marks < 90 RETURNING student_id, marks").fetchall()
print("deleted:", gone)
con.execute("DELETE FROM karachi_students")            # all rows (T-SQL: TRUNCATE TABLE is faster)
show(con, "SELECT COUNT(*) AS left_rows FROM karachi_students")

# %% [markdown]
# ## Example 6 - UPSERT (T-SQL: MERGE): insert new rows, update existing ones

# %%
incoming = [(101, "SQL", 84), (106, "SQL", 70)]          # 101/SQL exists, 106/SQL is new
con.executemany("""INSERT INTO marks (student_id, subject, marks) VALUES (?, ?, ?)
ON CONFLICT (student_id, subject) DO UPDATE SET marks = excluded.marks""", incoming)
show(con, "SELECT * FROM marks WHERE subject = 'SQL' AND student_id IN (101, 106)")

# %% [markdown]
# ## Example 7 - transactions: all or nothing

# %%
def transfer_batch(con, student_id, new_batch):
    try:
        con.execute("BEGIN")
        con.execute("UPDATE students SET batch_id = ? WHERE student_id = ?", (new_batch, student_id))
        con.execute("INSERT INTO marks VALUES (?, 'Orientation', 120)", (student_id,))   # breaks CHECK
        con.execute("COMMIT")
    except sqlite3.IntegrityError as e:
        con.execute("ROLLBACK")
        print("rolled back:", e)

transfer_batch(con, 104, "AI-2601")
show(con, "SELECT student_id, batch_id FROM students WHERE student_id = 104")      # still DS-2601
