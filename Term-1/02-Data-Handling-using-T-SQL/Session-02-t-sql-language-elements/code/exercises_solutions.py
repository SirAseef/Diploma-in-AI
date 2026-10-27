"""Session 02 - practice exercise solutions."""
# notebook: run-in-code-dir
from campus_db import connect, show

con = connect()
# 1. Faculty earning between 160,000 and 200,000, highest first
ex1 = show(con, "SELECT name, salary FROM faculty WHERE salary BETWEEN 160000 AND 200000 ORDER BY salary DESC")
# 2. Students whose email ends with example.com and whose city is known
ex2 = show(con, "SELECT name, email FROM students WHERE email LIKE '%@example.com' AND city IS NOT NULL")
# 3. Each student's average marks, only those averaging below 65
ex3 = show(con, """SELECT student_id, ROUND(AVG(marks), 1) AS avg_marks FROM marks
                   GROUP BY student_id HAVING AVG(marks) < 65 ORDER BY avg_marks""")
# 4. The two most recently joined students
ex4 = show(con, "SELECT name, joined_on FROM students ORDER BY joined_on DESC LIMIT 2")

if __name__ == "__main__":
    assert [r[0] for r in ex1] == ["Sana Iqbal", "Mehwish Raza", "Usman Tariq"]
    assert len(ex2) == 6
    assert [r[0] for r in ex3] == [108, 104, 102]
    assert ex4[0][0] == "Saad Qureshi"
    print("all exercise checks passed")
