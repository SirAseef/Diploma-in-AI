"""Session 07 - a small Flask app. Run: python app.py  then open http://127.0.0.1:5000"""
# build: no-run (starts a web server; tested through examples.py)
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Hello, Flask!</h1><p>Try /courses, /square/7, /search?q=python, /feedback, /api/courses</p>"


@app.route("/square/<int:n>")
def square(n):
    return f"{n} squared is {n * n}"


@app.route("/search")
def search():
    q = request.args.get("q", "")
    return f"You searched for: {q}"


@app.route("/courses")
def courses():
    return render_template("index.html", courses=["Python", "SQL", "MongoDB"])


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    message = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        message = f"Thank you, {name}!" if name else "Name is required."
    return render_template("feedback.html", message=message)


@app.route("/api/courses")
def api_courses():
    return jsonify([{"id": 1, "title": "Python"}, {"id": 2, "title": "SQL"}])


if __name__ == "__main__":
    app.run(debug=True)
