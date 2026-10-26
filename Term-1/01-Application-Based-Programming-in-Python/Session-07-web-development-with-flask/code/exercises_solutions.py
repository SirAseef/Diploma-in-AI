"""Session 07 practice solutions (with tests)."""
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route("/about")
def about():
    return "Aseef's student - Batch 2511C"


@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    return str(a + b)


@app.route("/api/grade")
def api_grade():
    marks = request.args.get("marks", type=int)
    if marks is None:
        return jsonify(error="marks is required"), 400
    g = "A" if marks >= 80 else "B" if marks >= 65 else "C" if marks >= 50 else "F"
    return jsonify(marks=marks, grade=g)


@app.route("/students")
def students():
    data = [{"name": "Ali", "marks": 72}, {"name": "Sana", "marks": 91}]
    return render_template("students.html", students=data)


if __name__ == "__main__":
    c = app.test_client()
    assert "2511C" in c.get("/about").get_data(as_text=True)
    assert c.get("/add/2/3").get_data(as_text=True) == "5"
    assert c.get("/api/grade?marks=72").get_json() == {"marks": 72, "grade": "B"}
    assert c.get("/api/grade").status_code == 400
    assert "<td>Sana</td>" in c.get("/students").get_data(as_text=True)
    print("All exercise routes work.")
