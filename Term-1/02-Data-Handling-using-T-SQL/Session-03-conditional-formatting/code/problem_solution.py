"""Real-life problem: print-ready result card for every mark entry, plus a status per student.
Rules: grade A >= 80, B >= 65, C >= 50, else F. Remark: A 'Excellent', B 'Good', C 'Needs practice', F 'Re-sit required'.
A student is 'Promoted' if no subject is below 50, otherwise 'Re-sit'. Students with no marks show 'No result'."""
# notebook: run-in-code-dir
from campus_db import connect, show

CARD = """
SELECT s.name,
       m.subject,
       printf('%3d / 100', m.marks) AS score,
       CASE WHEN m.marks >= 80 THEN 'A' WHEN m.marks >= 65 THEN 'B'
            WHEN m.marks >= 50 THEN 'C' ELSE 'F' END AS grade,
       CASE WHEN m.marks >= 80 THEN 'Excellent' WHEN m.marks >= 65 THEN 'Good'
            WHEN m.marks >= 50 THEN 'Needs practice' ELSE 'Re-sit required' END AS remark
FROM marks AS m, students AS s
WHERE s.student_id = m.student_id
ORDER BY s.name, m.subject
"""

STATUS = """
SELECT name,
       CASE
           WHEN (SELECT COUNT(*) FROM marks m WHERE m.student_id = s.student_id) = 0 THEN 'No result'
           WHEN (SELECT MIN(marks) FROM marks m WHERE m.student_id = s.student_id) < 50 THEN 'Re-sit'
           ELSE 'Promoted'
       END AS status
FROM students AS s
ORDER BY CASE status WHEN 'Re-sit' THEN 0 WHEN 'Promoted' THEN 1 ELSE 2 END, name
"""

if __name__ == "__main__":
    con = connect()
    card = show(con, CARD)
    status = dict(show(con, STATUS))
    assert len(card) == 16
    assert status["Ali Raza"] == "Re-sit" and status["Omar Farooq"] == "Re-sit"
    assert status["Saad Qureshi"] == "No result" and status["Hira Siddiqui"] == "Promoted"
    print("result cards OK")
