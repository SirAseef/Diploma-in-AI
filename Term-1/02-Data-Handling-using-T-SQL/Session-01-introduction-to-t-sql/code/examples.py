"""Session 01 - Introduction to Transact-SQL: worked examples.
We practise with SQLite (built into Python). The README shows the SQL Server (T-SQL) version of each query."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - connect to the sample campus database and list its tables

# %%
import sqlite3
from campus_db import connect, show

con = connect()
show(con, "SELECT name AS table_name FROM sqlite_master WHERE type = 'table' ORDER BY name")
# T-SQL: SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES;

# %% [markdown]
# ## Example 2 - DDL: create a table with data types and constraints

# %%
con.execute("""
CREATE TABLE courses (
    course_code  TEXT    PRIMARY KEY,           -- T-SQL: VARCHAR(10) NOT NULL PRIMARY KEY
    title        TEXT    NOT NULL,              -- T-SQL: NVARCHAR(80) NOT NULL
    duration_wk  INTEGER CHECK (duration_wk > 0),
    fee          INTEGER DEFAULT 0
)""")
show(con, "PRAGMA table_info(courses)")          # T-SQL: EXEC sp_help 'dbo.courses';

# %% [markdown]
# ## Example 3 - DML: insert and read rows

# %%
con.executemany("INSERT INTO courses VALUES (?, ?, ?, ?)", [
    ("DAI", "Diploma in AI", 48, 180000),
    ("DS", "Data Science", 24, 90000),
    ("PY", "Python Basics", 8, 25000),
])
show(con, "SELECT * FROM courses")
show(con, "SELECT title, fee FROM courses WHERE fee > 50000")

# %% [markdown]
# ## Example 4 - constraints protect the data

# %%
for bad in [("PY", "Duplicate code", 4, 0), ("XX", None, 4, 0), ("YY", "Negative", -2, 0)]:
    try:
        con.execute("INSERT INTO courses VALUES (?, ?, ?, ?)", bad)
    except sqlite3.IntegrityError as e:
        print(f"{bad[0]}: rejected -> {e}")

# %% [markdown]
# ## Example 5 - your first real queries on the campus data

# %%
show(con, "SELECT name, city FROM students")
show(con, "SELECT name, city, fee_paid FROM students WHERE city = 'Karachi' ORDER BY fee_paid DESC")
show(con, "SELECT COUNT(*) AS total_students FROM students")

# %% [markdown]
# ## Example 6 - DCL / TCL: a transaction you can roll back

# %%
con.execute("BEGIN")                                  # T-SQL: BEGIN TRANSACTION;
con.execute("DELETE FROM courses")
print("inside transaction:", con.execute("SELECT COUNT(*) FROM courses").fetchone()[0])
con.execute("ROLLBACK")                               # T-SQL: ROLLBACK TRANSACTION;
print("after rollback   :", con.execute("SELECT COUNT(*) FROM courses").fetchone()[0])
