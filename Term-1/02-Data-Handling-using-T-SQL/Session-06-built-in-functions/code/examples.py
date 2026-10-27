"""Session 06 - Working with Built-in Functions: worked examples (SQLite; T-SQL in README).
A fixed 'today' of 2026-10-27 keeps the outputs repeatable."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - string functions

# %%
from campus_db import connect, show
con = connect()
TODAY = "2026-10-27"
show(con, """SELECT name,
       UPPER(name)                               AS upper_name,
       LENGTH(name)                              AS len,
       SUBSTR(name, 1, INSTR(name, ' ') - 1)     AS first_name,
       SUBSTR(name, INSTR(name, ' ') + 1)        AS last_name,
       REPLACE(COALESCE(email, ''), '@example.com', '@campus.pk') AS new_email,
       TRIM('  ' || city || '  ')                AS city_trimmed
FROM students LIMIT 5""")

# %% [markdown]
# ## Example 2 - date functions

# %%
show(con, """SELECT name, joined_on,
       CAST(julianday(?) - julianday(joined_on) AS INTEGER)  AS days_enrolled,
       strftime('%Y', joined_on)                             AS join_year,
       strftime('%m', joined_on)                             AS join_month,
       date(joined_on, '+6 months')                          AS review_date,
       date(joined_on, 'start of month', '+1 month', '-1 day') AS month_end
FROM students ORDER BY joined_on LIMIT 5""", (TODAY,))

# %% [markdown]
# ## Example 3 - mathematical functions

# %%
show(con, """SELECT name, salary,
       ROUND(salary / 12.0, 2)        AS monthly,
       ROUND(salary * 0.075)          AS tax_estimate,
       CAST(salary / 1000 AS INTEGER) AS thousands_floor,
       ABS(salary - 180000)           AS distance_from_180k,
       salary % 7                     AS mod7
FROM faculty""")
show(con, "SELECT ROUND(AVG(marks), 2) AS mean, MAX(marks) - MIN(marks) AS range_, SQRT(AVG(marks*marks) - AVG(marks)*AVG(marks)) AS std_dev FROM marks")

# %% [markdown]
# ## Example 4 - aggregate and conversion functions together

# %%
show(con, """SELECT b.course,
       COUNT(s.student_id)                       AS students,
       SUM(s.fee_paid)                           AS collected,
       'Rs ' || format('%,d', SUM(s.fee_paid))   AS collected_text,
       group_concat(s.name, ', ')                AS names      -- T-SQL: STRING_AGG(s.name, ', ')
FROM batches b LEFT JOIN students s ON s.batch_id = b.batch_id
GROUP BY b.course""")

# %% [markdown]
# ## Example 5 - ranking (window) functions

# %%
show(con, """SELECT subject, student_id, marks,
       ROW_NUMBER() OVER (PARTITION BY subject ORDER BY marks DESC) AS row_no,
       RANK()       OVER (PARTITION BY subject ORDER BY marks DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY marks DESC)                      AS overall_dense,
       NTILE(4)     OVER (ORDER BY marks DESC)                      AS quartile
FROM marks ORDER BY subject, row_no""")

# %% [markdown]
# ## Example 6 - aggregate window functions: running totals and share of total

# %%
show(con, """SELECT name, joined_on, fee_paid,
       SUM(fee_paid) OVER (ORDER BY joined_on)                         AS running_total,
       ROUND(100.0 * fee_paid / SUM(fee_paid) OVER (), 1)              AS pct_of_all,
       fee_paid - AVG(fee_paid) OVER (PARTITION BY batch_id)           AS vs_batch_avg,
       LAG(name) OVER (ORDER BY joined_on)                             AS joined_after
FROM students ORDER BY joined_on""")
