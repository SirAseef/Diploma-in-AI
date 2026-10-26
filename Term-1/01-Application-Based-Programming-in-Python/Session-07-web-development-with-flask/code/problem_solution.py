"""Real-life problem: course feedback JSON API (app-factory pattern) + self-tests."""
from flask import Flask, jsonify, request


def create_app():
    app = Flask(__name__)
    store = []

    @app.post("/api/feedback")
    def add_feedback():
        data = request.get_json(silent=True) or {}
        rating = data.get("rating")
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            return jsonify(error="rating must be an integer 1-5"), 400
        item = {"id": len(store) + 1, "rating": rating, "comment": data.get("comment", "")}
        store.append(item)
        return jsonify(item), 201

    @app.get("/api/feedback/summary")
    def summary():
        if not store:
            return jsonify(count=0, average=None)
        avg = round(sum(i["rating"] for i in store) / len(store), 2)
        return jsonify(count=len(store), average=avg)

    return app


if __name__ == "__main__":
    c = create_app().test_client()
    assert c.get("/api/feedback/summary").get_json() == {"count": 0, "average": None}
    for rating in (5, 4, 4):
        assert c.post("/api/feedback", json={"rating": rating, "comment": "good"}).status_code == 201
    assert c.post("/api/feedback", json={"rating": 9}).status_code == 400
    assert c.post("/api/feedback", data="not json").status_code == 400
    s = c.get("/api/feedback/summary").get_json()
    print(s)
    assert s == {"count": 3, "average": 4.33}
    print("All feedback API tests passed. Run create_app().run(debug=True) to serve it.")
