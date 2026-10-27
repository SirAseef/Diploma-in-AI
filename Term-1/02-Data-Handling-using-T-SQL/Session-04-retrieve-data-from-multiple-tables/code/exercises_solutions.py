"""Session 04 - practice exercise solutions."""
# notebook: run-in-code-dir
from campus_db import connect, show

con = connect()
# 1. Each mark with the student's name and city
ex1 = show(con, """SELECT s.name, s.city, m.subject, m.marks
FROM marks m JOIN students s ON s.student_id = m.student_id ORDER BY s.name, m.subject""")
# 2. Number of students per course, including courses with zero students
ex2 = show(con, """SELECT b.course, COUNT(s.student_id) AS students
FROM batches b LEFT JOIN students s ON s.batch_id = b.batch_id
GROUP BY b.course ORDER BY students DESC, b.course""")
# 3. Average marks per teacher (through batch -> students -> marks)
ex3 = show(con, """SELECT f.name AS teacher, ROUND(AVG(m.marks), 1) AS avg_marks
FROM faculty f
JOIN batches b  ON b.faculty_id = f.faculty_id
JOIN students s ON s.batch_id = b.batch_id
JOIN marks m    ON m.student_id = s.student_id
GROUP BY f.name ORDER BY avg_marks DESC""")
# 4. Students who scored above their own batch's average in Python (correlated subquery)
ex4 = show(con, """SELECT s.name, s.batch_id, m.marks FROM students s JOIN marks m ON m.student_id = s.student_id
WHERE m.subject = 'Python' AND m.marks > (
    SELECT AVG(m2.marks) FROM marks m2 JOIN students s2 ON s2.student_id = m2.student_id
    WHERE s2.batch_id = s.batch_id AND m2.subject = 'Python')""")

if __name__ == "__main__":
    assert len(ex1) == 16
    assert ("Machine Learning", 0) in ex2 and ex2[0] == ("Diploma in AI", 5)
    assert ex3[0][0] == "Usman Tariq"
    assert {r[0] for r in ex4} == {"Ayesha Khan", "Bilal Ahmed", "Hira Siddiqui", "Zara Hussain"}
    print("all exercise checks passed")
