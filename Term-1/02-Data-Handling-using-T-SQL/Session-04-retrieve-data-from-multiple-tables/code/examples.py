"""Session 04 - Retrieve Data from Multiple Tables: worked examples (SQLite; T-SQL in README).
RIGHT and FULL OUTER JOIN need SQLite 3.39+ (bundled with recent Python)."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - INNER JOIN: students with their batch and course

# %%
from campus_db import connect, show
con = connect()
show(con, """SELECT s.name, s.batch_id, b.course, b.timing
FROM students AS s
INNER JOIN batches AS b ON b.batch_id = s.batch_id
ORDER BY b.course, s.name""")

# %% [markdown]
# ## Example 2 - joining three tables

# %%
show(con, """SELECT s.name AS student, b.course, f.name AS teacher
FROM students s
JOIN batches  b ON b.batch_id   = s.batch_id
JOIN faculty  f ON f.faculty_id = b.faculty_id
ORDER BY teacher, student""")

# %% [markdown]
# ## Example 3 - LEFT JOIN keeps rows with no match (find who is missing)

# %%
show(con, """SELECT s.name, COALESCE(b.course, '-- not placed --') AS course
FROM students s LEFT JOIN batches b ON b.batch_id = s.batch_id""")
show(con, """SELECT b.batch_id, b.course
FROM batches b LEFT JOIN students s ON s.batch_id = b.batch_id
WHERE s.student_id IS NULL""")                     # batches with no students yet

# %% [markdown]
# ## Example 4 - RIGHT and FULL OUTER JOIN

# %%
show(con, """SELECT f.name AS teacher, b.batch_id
FROM batches b RIGHT JOIN faculty f ON f.faculty_id = b.faculty_id""")
show(con, """SELECT f.name AS teacher, b.batch_id
FROM faculty f FULL OUTER JOIN batches b ON b.faculty_id = f.faculty_id
ORDER BY teacher""")

# %% [markdown]
# ## Example 5 - self join and CROSS JOIN

# %%
show(con, """SELECT a.name AS student, b.name AS classmate, a.batch_id
FROM students a JOIN students b ON a.batch_id = b.batch_id AND a.student_id < b.student_id
ORDER BY a.batch_id""")
show(con, """SELECT f.name, t.slot FROM faculty f
CROSS JOIN (SELECT 'Morning' AS slot UNION ALL SELECT 'Evening') AS t
WHERE f.subject IN ('Python', 'SQL')""")

# %% [markdown]
# ## Example 6 - set operators: UNION, UNION ALL, INTERSECT, EXCEPT

# %%
show(con, """SELECT name, 'student' AS role FROM students WHERE city = 'Lahore'
UNION
SELECT name, 'faculty' FROM faculty WHERE subject = 'SQL'""")
show(con, "SELECT student_id FROM marks WHERE subject = 'Python' INTERSECT SELECT student_id FROM marks WHERE subject = 'SQL'")
show(con, "SELECT student_id FROM students EXCEPT SELECT student_id FROM marks")      # no marks yet

# %% [markdown]
# ## Example 7 - subqueries: scalar, IN, EXISTS and correlated

# %%
show(con, "SELECT student_id, subject, marks FROM marks WHERE marks > (SELECT AVG(marks) FROM marks)")
show(con, "SELECT name FROM students WHERE batch_id IN (SELECT batch_id FROM batches WHERE timing = 'Evening')")
show(con, "SELECT f.name FROM faculty f WHERE NOT EXISTS (SELECT 1 FROM batches b WHERE b.faculty_id = f.faculty_id)")
show(con, """SELECT m.student_id, m.subject, m.marks FROM marks m
WHERE m.marks = (SELECT MAX(m2.marks) FROM marks m2 WHERE m2.subject = m.subject)""")  # topper per subject
