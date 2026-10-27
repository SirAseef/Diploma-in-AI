"""Real-life problem: one 'student 360' report for the centre manager, joining all four tables.
For every student (including those not yet in a batch): course, teacher, subjects attempted,
average marks, a flag if any subject is failed, and fee balance. Then list teachers whose
batches have the most at-risk students (failed a subject OR fee balance > 15,000)."""
# notebook: run-in-code-dir
from campus_db import connect, show

FEE = 45000

STUDENT_360 = """
SELECT s.student_id,
       s.name,
       COALESCE(b.course, 'Not placed')       AS course,
       COALESCE(f.name, '-')                  AS teacher,
       COUNT(m.subject)                       AS subjects,
       ROUND(AVG(m.marks), 1)                 AS avg_marks,
       MAX(CASE WHEN m.marks < 50 THEN 1 ELSE 0 END) AS failed_any,
       ? - s.fee_paid                         AS fee_balance
FROM students s
LEFT JOIN batches b ON b.batch_id   = s.batch_id
LEFT JOIN faculty f ON f.faculty_id = b.faculty_id
LEFT JOIN marks   m ON m.student_id = s.student_id
GROUP BY s.student_id, s.name, b.course, f.name, s.fee_paid
ORDER BY s.student_id
"""

AT_RISK_BY_TEACHER = """
WITH report AS (
    SELECT s.student_id, b.faculty_id,
           MAX(CASE WHEN m.marks < 50 THEN 1 ELSE 0 END) AS failed_any,
           ? - s.fee_paid AS fee_balance
    FROM students s
    JOIN batches b     ON b.batch_id   = s.batch_id
    LEFT JOIN marks m  ON m.student_id = s.student_id
    GROUP BY s.student_id, b.faculty_id, s.fee_paid
)
SELECT f.name AS teacher, COUNT(*) AS at_risk
FROM report r JOIN faculty f ON f.faculty_id = r.faculty_id
WHERE r.failed_any = 1 OR r.fee_balance > 15000
GROUP BY f.name
ORDER BY at_risk DESC, teacher
"""

if __name__ == "__main__":
    con = connect()
    rows = show(con, STUDENT_360, (FEE,))
    risk = show(con, AT_RISK_BY_TEACHER, (FEE,))
    by_id = {r[0]: r for r in rows}
    assert len(rows) == 10                                   # every student, even 110 with no batch
    assert by_id[110][2] == "Not placed" and by_id[110][4] == 0
    assert by_id[108][6] == 1 and by_id[103][6] == 0
    assert risk[0] == ("Kamran Ali", 2) and len(risk) == 3
    print("student 360 OK")
