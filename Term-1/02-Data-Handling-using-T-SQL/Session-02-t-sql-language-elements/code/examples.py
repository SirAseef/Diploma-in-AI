"""Session 02 - T-SQL Language Elements: worked examples (SQLite; T-SQL shown in README)."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - columns, expressions and aliases

# %%
from campus_db import connect, show
con = connect()
show(con, """SELECT name,
                    fee_paid,
                    45000 - fee_paid AS balance,
                    ROUND(fee_paid * 100.0 / 45000, 1) AS pct_paid
             FROM students""")

# %% [markdown]
# ## Example 2 - WHERE with comparison, logical, BETWEEN, IN, LIKE, IS NULL

# %%
show(con, "SELECT name, city FROM students WHERE city = 'Karachi' AND fee_paid >= 45000")
show(con, "SELECT student_id, subject, marks FROM marks WHERE marks BETWEEN 60 AND 80")
show(con, "SELECT name, city FROM students WHERE city IN ('Lahore', 'Islamabad')")
show(con, "SELECT name FROM students WHERE name LIKE 'H%'")          # starts with H
show(con, "SELECT name FROM students WHERE email IS NULL")

# %% [markdown]
# ## Example 3 - DISTINCT, ORDER BY and paging (LIMIT/OFFSET = T-SQL TOP / OFFSET-FETCH)

# %%
show(con, "SELECT DISTINCT city FROM students WHERE city IS NOT NULL ORDER BY city")
show(con, "SELECT student_id, subject, marks FROM marks ORDER BY marks DESC LIMIT 3")
show(con, "SELECT student_id, name FROM students ORDER BY student_id LIMIT 3 OFFSET 3")  # page 2

# %% [markdown]
# ## Example 4 - aggregates with GROUP BY and HAVING

# %%
show(con, """SELECT subject, COUNT(*) AS attempts, ROUND(AVG(marks), 1) AS avg_marks,
                    MIN(marks) AS lowest, MAX(marks) AS highest
             FROM marks
             GROUP BY subject
             ORDER BY avg_marks DESC""")
show(con, """SELECT city, COUNT(*) AS students
             FROM students
             WHERE city IS NOT NULL
             GROUP BY city
             HAVING COUNT(*) >= 2""")

# %% [markdown]
# ## Example 5 - variables and parameters
# T-SQL uses DECLARE @city NVARCHAR(40) = N'Karachi'. From Python we pass parameters with ? placeholders.

# %%
city, min_fee = "Karachi", 20000
show(con, "SELECT name, fee_paid FROM students WHERE city = ? AND fee_paid >= ?", (city, min_fee))
