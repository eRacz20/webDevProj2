from flask import Flask, request, jsonify
from flask_cors import CORS
import os, psycopg2

app = Flask(__name__)
CORS(app)

def db():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

# ---------- CREATE TABLE + SEED ----------
def init_db():
    conn=db()
    cur=conn.cursor()

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

    cur.execute("SELECT COUNT(*) FROM movies")
    count=cur.fetchone()[0]

    if count < 30:
        cur.execute("DELETE FROM movies")

        movies=[
("Inception",2010,"Sci-Fi",9,"https://via.placeholder.com/120x180"),
("Titanic",1997,"Romance",8,"https://via.placeholder.com/120x180"),
("The Matrix",1999,"Sci-Fi",10,"https://via.placeholder.com/120x180"),
("Avatar",2009,"Fantasy",7,"https://via.placeholder.com/120x180"),
("Toy Story",1995,"Animation",9,"https://via.placeholder.com/120x180"),
("The Dark Knight",2008,"Action",10,"https://via.placeholder.com/120x180"),
("Forrest Gump",1994,"Drama",9,"https://via.placeholder.com/120x180"),
("Gladiator",2000,"Action",9,"https://via.placeholder.com/120x180"),
("Interstellar",2014,"Sci-Fi",9,"https://via.placeholder.com/120x180"),
("Joker",2019,"Drama",8,"https://via.placeholder.com/120x180"),
("Frozen",2013,"Animation",7,"https://via.placeholder.com/120x180"),
("Up",2009,"Animation",9,"https://via.placeholder.com/120x180"),
("Iron Man",2008,"Action",8,"https://via.placeholder.com/120x180"),
("Black Panther",2018,"Action",8,"https://via.placeholder.com/120x180"),
("Finding Nemo",2003,"Animation",9,"https://via.placeholder.com/120x180"),
("Cars",2006,"Animation",7,"https://via.placeholder.com/120x180"),
("The Lion King",1994,"Animation",10,"https://via.placeholder.com/120x180"),
("Shrek",2001,"Animation",8,"https://via.placeholder.com/120x180"),
("Harry Potter 1",2001,"Fantasy",8,"https://via.placeholder.com/120x180"),
("Harry Potter 2",2002,"Fantasy",8,"https://via.placeholder.com/120x180"),
("Harry Potter 3",2004,"Fantasy",9,"https://via.placeholder.com/120x180"),
("Spider-Man",2002,"Action",7,"https://via.placeholder.com/120x180"),
("Spider-Man 2",2004,"Action",9,"https://via.placeholder.com/120x180"),
("Spider-Man 3",2007,"Action",6,"https://via.placeholder.com/120x180"),
("Doctor Strange",2016,"Action",8,"https://via.placeholder.com/120x180"),
("Thor",2011,"Action",7,"https://via.placeholder.com/120x180"),
("Captain America",2011,"Action",7,"https://via.placeholder.com/120x180"),
("Deadpool",2016,"Action",8,"https://via.placeholder.com/120x180"),
("Logan",2017,"Action",9,"https://via.placeholder.com/120x180"),
("The Avengers",2012,"Action",9,"https://via.placeholder.com/120x180")
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

@app.route("/")
def home():
    return "Movie API running"

# ---------- GET MOVIES ----------
@app.route("/movies")
def get_movies():
    search=request.args.get("search","")
    rating=request.args.get("rating","")

    conn=db()
    cur=conn.cursor()

    query="SELECT * FROM movies WHERE 1=1"
    params=[]

    if search:
        query+=" AND LOWER(title) LIKE %s"
        params.append(f"%{search.lower()}%")

    if rating:
        query+=" AND rating >= %s"
        params.append(rating)

    query+=" ORDER BY title"
    cur.execute(query,params)

    rows=cur.fetchall()

    movies=[{
        "id":r[0],
        "title":r[1],
        "year":r[2],
        "genre":r[3],
        "rating":r[4],
        "image_url":r[5]
    } for r in rows]

    return jsonify({"movies":movies})

# ---------- ADD ----------
@app.route("/movies",methods=["POST"])
def add_movie():
    d=request.json
    conn=db();cur=conn.cursor()
    cur.execute("""
        INSERT INTO movies(title,year,genre,rating,image_url)
        VALUES(%s,%s,%s,%s,%s)
    """,(d["title"],d["year"],d["genre"],d["rating"],d["image_url"]))
    conn.commit()
    return {"msg":"added"}

# ---------- EDIT ----------
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
    return {"msg":"updated"}

# ---------- DELETE ----------
@app.route("/movies/<int:id>",methods=["DELETE"])
def delete_movie(id):
    conn=db();cur=conn.cursor()
    cur.execute("DELETE FROM movies WHERE id=%s",(id,))
    conn.commit()
    return {"msg":"deleted"}

# ---------- STATS ----------
@app.route("/stats")
def stats():
    conn=db()
    cur=conn.cursor()
    cur.execute("SELECT COUNT(*), AVG(rating) FROM movies")
    total,avg=cur.fetchone()
    return jsonify({"total":total,"avg_rating":round(avg,2)})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.getenv("PORT",5000)))