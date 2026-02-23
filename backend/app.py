from flask import Flask, request, jsonify
from flask_cors import CORS
import os, psycopg2

app = Flask(__name__)
CORS(app)

def db():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

# ---------- CREATE TABLE IF NOT EXISTS ----------
def init_db():
    conn = db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies(
            id SERIAL PRIMARY KEY,
            title TEXT,
            year INT,
            genre TEXT,
            rating INT,
            image_url TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.route("/")
def home():
    return "Movie API running"

# ---------- READ ----------
@app.route("/movies")
def get_movies():
    conn=db()
    cur=conn.cursor()

    cur.execute("SELECT * FROM movies ORDER BY id DESC")
    rows = cur.fetchall()

    movies=[{
        "id":r[0],
        "title":r[1],
        "year":r[2],
        "genre":r[3],
        "rating":r[4],
        "image_url":r[5]
    } for r in rows]

    cur.close()
    conn.close()
    return jsonify({"movies":movies})

# ---------- CREATE ----------
@app.route("/movies",methods=["POST"])
def add_movie():
    d=request.json
    conn=db();cur=conn.cursor()
    cur.execute("""
        INSERT INTO movies(title,year,genre,rating,image_url)
        VALUES(%s,%s,%s,%s,%s)
    """,(d["title"],d["year"],d["genre"],d["rating"],d["image_url"]))
    conn.commit()
    cur.close();conn.close()
    return {"msg":"added"}

# ---------- UPDATE ----------
@app.route("/movies/<int:id>",methods=["PUT"])
def edit_movie(id):
    d=request.json
    conn=db();cur=conn.cursor()
    cur.execute("""
        UPDATE movies
        SET title=%s,year=%s,genre=%s,rating=%s,image_url=%s
        WHERE id=%s
    """,(d["title"],d["year"],d["genre"],d["rating"],d["image_url"],id))
    conn.commit()
    cur.close();conn.close()
    return {"msg":"updated"}

# ---------- DELETE ----------
@app.route("/movies/<int:id>",methods=["DELETE"])
def delete_movie(id):
    conn=db();cur=conn.cursor()
    cur.execute("DELETE FROM movies WHERE id=%s",(id,))
    conn.commit()
    cur.close();conn.close()
    return {"msg":"deleted"}

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.getenv("PORT",5000)))