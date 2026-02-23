from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

# ---------- DB CONNECTION ----------

def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME", "MovieWebDB")
    )
# ---------- READ ----------
@app.route("/movies", methods=["GET"])
def get_movies():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM movies ORDER BY id DESC")
    movies = cursor.fetchall()

    cursor.close()
    db.close()
    return jsonify(movies)

# ---------- CREATE ----------
@app.route("/movies", methods=["POST"])
def add_movie():
    data = request.json

    db = get_db()
    cursor = db.cursor()

    sql = """
        INSERT INTO movies (title, genre, year, rating, image_url)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        data["title"],
        data["genre"],
        data["year"],
        data["rating"],
        data.get("image_url", "")
    ))

    db.commit()
    cursor.close()
    db.close()

    return {"message": "Movie added"}, 201

# ---------- UPDATE ----------
@app.route("/movies/<int:id>", methods=["PUT"])
def update_movie(id):
    data = request.json

    db = get_db()
    cursor = db.cursor()

    sql = """
        UPDATE movies
        SET title=%s, genre=%s, year=%s, rating=%s, image_url=%s
        WHERE id=%s
    """
    cursor.execute(sql, (
        data["title"],
        data["genre"],
        data["year"],
        data["rating"],
        data.get("image_url", ""),
        id
    ))

    db.commit()
    cursor.close()
    db.close()

    return {"message": "Movie updated"}

# ---------- DELETE ----------
@app.route("/movies/<int:id>", methods=["DELETE"])
def delete_movie(id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM movies WHERE id=%s", (id,))
    db.commit()

    cursor.close()
    db.close()

    return {"message": "Deleted"}

if __name__ == "__main__":
    app.run(debug=True)