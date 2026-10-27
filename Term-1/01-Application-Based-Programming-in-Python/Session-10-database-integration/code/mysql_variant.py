"""Session 10 - the same CRUD flow on MySQL with mysql-connector-python.
Needs a running MySQL server:  pip install mysql-connector-python
Set credentials in environment variables (never hard-code passwords):
    MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DB
"""
# build: no-run
import os
import mysql.connector
from mysql.connector import Error


def main():
    conn = mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ["MYSQL_PWD"],
        database=os.environ.get("MYSQL_DB", "school"),
    )
    cur = conn.cursor()
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS students(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(60) NOT NULL,
            city VARCHAR(40),
            marks INT CHECK (marks BETWEEN 0 AND 100))""")
        cur.executemany("INSERT INTO students(name, city, marks) VALUES (%s, %s, %s)",
                        [("Ayesha", "Karachi", 88), ("Bilal", "Lahore", 64), ("Hira", "Karachi", 92)])
        conn.commit()
        cur.execute("SELECT name, marks FROM students WHERE city = %s ORDER BY marks DESC", ("Karachi",))
        for name, marks in cur.fetchall():
            print(name, marks)
        cur.execute("UPDATE students SET marks = marks + 5 WHERE marks < %s", (70,))
        cur.execute("DELETE FROM students WHERE name = %s", ("Bilal",))
        conn.commit()
        print(cur.rowcount, "row(s) deleted")
    except Error as e:
        conn.rollback()
        print("MySQL error:", e)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
