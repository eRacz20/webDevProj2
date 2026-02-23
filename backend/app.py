from flask import Flask, request, jsonify
from flask_cors import CORS
import os, psycopg2

app = Flask(__name__)
CORS(app)

# ---------------- DB CONNECTION ----------------
def db():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

# ---------------- CREATE TABLE + SEED ----------------
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

    cur.execute("SELECT COUNT(*) FROM movies;")
    count = cur.fetchone()[0]

    if count == 0:
        print("Seeding movies...")
        movies = [
            ("Inception",2010,"Sci-Fi",9,"https://via.placeholder.com/120x180"),
            ("Titanic",1997,"Romance",8,"https://via.placeholder.com/120x180"),
            ("The Matrix",1999,"Sci-Fi",10,"https://via.placeholder.com/120x180"),
            ("Avatar",2009,"Fantasy",7,"https://via.placeholder.com/120x180"),
            ("Toy Story",1995,"Animation",9,"https://via.placeholder.com/120x180"),
        ]

        for m in movies:
            cur.execute(
                "INSERT INTO movies(title,year,genre,rating,image_url) VALUES(%s,%s,%s,%s,%s)",
                m
            )

        conn.commit()

    cur.close()
    conn.close()

init_db()

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return "Movie API running"

@app.route("/movies")
def get_movies():
    page = int(request.args.get("page",1))
    size = int(request.args.get("size",10))
    search = request.args.get("search","")

    offset = (page-1)*size

    conn=db()
    cur=conn.cursor()

    cur.execute("""
        SELECT * FROM movies
        WHERE title ILIKE %s
        ORDER BY title
        LIMIT %s OFFSET %s
    """,(f"%{search}%",size,offset))

    movies = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM movies")
    total = cur.fetchone()[0]

    cur.close()
    conn.close()

    result = [
        {"id":m[0],"title":m[1],"year":m[2],"genre":m[3],"rating":m[4],"image_url":m[5]}
        for m in movies
    ]

    return jsonify({"movies":result,"total":total})

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

@app.route("/movies/<int:id>",methods=["DELETE"])
def delete_movie(id):
    conn=db();cur=conn.cursor()
    cur.execute("DELETE FROM movies WHERE id=%s",(id,))
    conn.commit()
    cur.close();conn.close()
    return {"msg":"deleted"}

@app.route("/stats")
def stats():
    conn=db();cur=conn.cursor()
    cur.execute("SELECT COUNT(*), AVG(rating) FROM movies")
    total, avg = cur.fetchone()
    cur.close();conn.close()
    return jsonify({"total":total,"avg_rating":avg})

# ---------------- RUN LOCAL ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))