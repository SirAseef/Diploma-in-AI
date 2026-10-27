"""Session 03 - Performing Conditional Formatting: worked examples (SQLite; T-SQL in README).
Needs SQLite 3.32+ for IIF (bundled with Python 3.9+)."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - searched CASE: turn marks into grades

# %%
from campus_db import connect, show
con = connect()
show(con, """SELECT student_id, subject, marks,
       CASE
           WHEN marks >= 80 THEN 'A'
           WHEN marks >= 65 THEN 'B'
           WHEN marks >= 50 THEN 'C'
           ELSE 'F'
       END AS grade
FROM marks ORDER BY marks DESC""")

# %% [markdown]
# ## Example 2 - simple CASE: translate codes into friendly text

# %%
show(con, """SELECT batch_id,
       CASE timing
           WHEN 'Morning' THEN '9 am - 12 pm'
           WHEN 'Evening' THEN '6 pm - 9 pm'
           WHEN 'Weekend' THEN 'Sat & Sun'
           ELSE 'To be announced'
       END AS class_time
FROM batches""")

# %% [markdown]
# ## Example 3 - IIF for a quick two-way choice

# %%
show(con, "SELECT name, fee_paid, IIF(fee_paid >= 45000, 'Cleared', 'Pending') AS fee_status FROM students")

# %% [markdown]
# ## Example 4 - handling NULLs: COALESCE and NULLIF

# %%
show(con, """SELECT name,
       COALESCE(email, 'no email on file') AS contact,
       COALESCE(city, 'Unknown')           AS city,
       COALESCE(batch_id, 'Not placed')    AS batch
FROM students""")
show(con, "SELECT name, 45000 / NULLIF(fee_paid, 0) AS times_paid FROM students")   # avoids divide-by-zero

# %% [markdown]
# ## Example 5 - formatting output: CAST, rounding, number and text formats

# %%
show(con, """SELECT name,
       'Rs ' || format('%,d', fee_paid)                 AS fee_display,
       printf('%.1f%%', fee_paid * 100.0 / 45000)       AS paid_pct,
       CAST(fee_paid AS TEXT) || ' PKR'                 AS fee_text,
       UPPER(SUBSTR(name, 1, 1)) || '.'                 AS initial,
       strftime('%d-%m-%Y', joined_on)                  AS joined_pk
FROM students LIMIT 4""")

# %% [markdown]
# ## Example 6 - CASE inside aggregates and ORDER BY (a mini pivot)

# %%
show(con, """SELECT subject,
       SUM(CASE WHEN marks >= 50 THEN 1 ELSE 0 END) AS passed,
       SUM(CASE WHEN marks <  50 THEN 1 ELSE 0 END) AS failed,
       ROUND(100.0 * SUM(CASE WHEN marks >= 50 THEN 1 ELSE 0 END) / COUNT(*), 0) AS pass_rate
FROM marks GROUP BY subject""")
show(con, """SELECT name, city FROM students
ORDER BY CASE WHEN city = 'Karachi' THEN 0 WHEN city IS NULL THEN 2 ELSE 1 END, name""")
