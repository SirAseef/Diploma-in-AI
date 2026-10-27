"""Session 06 - practice exercise solutions."""
# notebook: run-in-code-dir
from campus_db import connect, show

con = connect()
TODAY = "2026-10-27"
# 1. Initials (first letter of each of two names) and name length, longest first
ex1 = show(con, """SELECT name, SUBSTR(name, 1, 1) || SUBSTR(name, INSTR(name, ' ') + 1, 1) AS initials, LENGTH(name) AS len
FROM students ORDER BY len DESC, name""")
# 2. Teachers' years of service (whole years) as of TODAY
ex2 = show(con, """SELECT name, CAST((julianday(?) - julianday(hired_on)) / 365.25 AS INTEGER) AS years
FROM faculty ORDER BY years DESC""", (TODAY,))
# 3. Students per joining month as 'YYYY-MM'
ex3 = show(con, "SELECT strftime('%Y-%m', joined_on) AS month, COUNT(*) AS joined FROM students GROUP BY month ORDER BY month")
# 4. The top scorer in every subject using ROW_NUMBER
ex4 = show(con, """SELECT subject, student_id, marks FROM (
    SELECT subject, student_id, marks, ROW_NUMBER() OVER (PARTITION BY subject ORDER BY marks DESC) AS rn FROM marks
) WHERE rn = 1 ORDER BY subject""")

if __name__ == "__main__":
    assert ex1[0][0] == "Hira Siddiqui" and ex1[0][1] == "HS"
    assert dict(ex2)["Usman Tariq"] == 7 and dict(ex2)["Nida Farooq"] == 2
    assert dict(ex3)["2026-01"] == 5
    assert ex4 == [("Python", 103, 92), ("SQL", 103, 95), ("Statistics", 105, 83), ("Web", 109, 90)]
    print("all exercise checks passed")
