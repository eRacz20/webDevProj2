from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

DATA_FILE = "movies.json"

def load_movies():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_movies(movies):
    with open(DATA_FILE, "w") as f:
        json.dump(movies, f, indent=2)

@app.route("/movies", methods=["GET"])
def get_movies():
    return jsonify(load_movies())

@app.route("/movies", methods=["POST"])
def add_movie():
    movies = load_movies()
    data = request.json

    if not data.get("title") or not data.get("genre"):
        return {"error": "Invalid data"}, 400

    new_id = max(m["id"] for m in movies) + 1
    data["id"] = new_id
    movies.append(data)
    save_movies(movies)

    return jsonify(data), 201

@app.route("/movies/<int:id>", methods=["PUT"])
def update_movie(id):
    movies = load_movies()
    data = request.json

    for movie in movies:
        if movie["id"] == id:
            movie.update(data)
            save_movies(movies)
            return jsonify(movie)

    return {"error": "Not found"}, 404

@app.route("/movies/<int:id>", methods=["DELETE"])
def delete_movie(id):
    movies = load_movies()
    movies = [m for m in movies if m["id"] != id]
    save_movies(movies)
    return "", 204

import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
