import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "mysql+pymysql://root:password@localhost/history_places"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(120))
    era = db.Column(db.String(100))
    description = db.Column(db.Text)

    def as_json(self):
        return {key: getattr(self, key) for key in ("id", "name", "country", "region", "era", "description")}


with app.app_context():
    db.create_all()


@app.get("/api/places")
def list_places():
    query = Place.query
    term = request.args.get("q", "").strip()
    if term:
        like = f"%{term}%"
        query = query.filter(db.or_(Place.name.ilike(like), Place.country.ilike(like), Place.region.ilike(like), Place.description.ilike(like)))
    return jsonify([place.as_json() for place in query.order_by(Place.name).all()])


@app.post("/api/places")
def create_place():
    data = request.get_json(silent=True) or {}
    name, country = data.get("name", "").strip(), data.get("country", "").strip()
    if not name or not country:
        return jsonify(error="name and country are required"), 400
    place = Place(name=name, country=country, region=data.get("region"), era=data.get("era"), description=data.get("description"))
    db.session.add(place)
    db.session.commit()
    return jsonify(place.as_json()), 201


@app.get("/api/places/<int:place_id>")
def get_place(place_id):
    place = db.session.get(Place, place_id)
    return (jsonify(place.as_json()), 200) if place else (jsonify(error="place not found"), 404)


@app.delete("/api/places/<int:place_id>")
def delete_place(place_id):
    place = db.session.get(Place, place_id)
    if not place:
        return jsonify(error="place not found"), 404
    db.session.delete(place)
    db.session.commit()
    return "", 204


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
