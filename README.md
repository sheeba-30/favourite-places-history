# Favourite Places in History

A small Python backend for saving and searching historically significant places. It exposes a JSON REST API backed by MySQL using SQLAlchemy.

## Run

1. Create a MySQL database named `history_places`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set `DATABASE_URL`, for example `mysql+pymysql://user:password@localhost/history_places`.
4. Run `python app.py` and open `http://localhost:5000`.

## API

- `GET /api/places?q=...` lists places or searches name, region, and historical notes.
- `POST /api/places` creates a place. Required JSON: `name`, `country`; optional: `region`, `era`, `description`.
- `GET /api/places/<id>` returns one place.
- `DELETE /api/places/<id>` removes one place.

## Stack

Python, Flask, SQLAlchemy, MySQL, REST, JSON
