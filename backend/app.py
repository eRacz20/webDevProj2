from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg2
import psycopg2.extras

app = Flask(__name__)
CORS(app)

# ---------- DB CONNECTION ----------
def db():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

# ---------- CREATE TABLE + SEED ----------
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

    cur.execute("SELECT COUNT(*) FROM movies")
    count = cur.fetchone()[0]

    if count < 30:
        cur.execute("DELETE FROM movies")

        movies = [
        ("The Dark Knight",2008,"Action",10,"https://image.tmdb.org/t/p/w200/qJ2tW6WMUDux911r6m7haRef0WH.jpg"),
        ("Inception",2010,"Sci-Fi",9,"https://image.tmdb.org/t/p/w200/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg"),
        ("Interstellar",2014,"Sci-Fi",10,"https://image.tmdb.org/t/p/w200/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"),
        ("Titanic",1997,"Romance",8,"https://image.tmdb.org/t/p/w200/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg"),
        ("The Matrix",1999,"Sci-Fi",10,"https://image.tmdb.org/t/p/w200/aOIuZAjPaRIE6CMzbazvcHuHXDc.jpg"),
        ("Avatar",2009,"Fantasy",7,"https://image.tmdb.org/t/p/w200/jRXYjXNq0Cs2TcJjLkki24MLp7u.jpg"),
        ("Fight Club",1999,"Drama",9,"https://image.tmdb.org/t/p/w200/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg"),
        ("Forrest Gump",1994,"Drama",10,"https://image.tmdb.org/t/p/w200/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg"),
        ("Gladiator",2000,"Action",9,"https://image.tmdb.org/t/p/w200/ty8TGRuvJLPUmAR1H1nRIsgwvim.jpg"),
        ("Jurassic Park",1993,"Adventure",9,"https://image.tmdb.org/t/p/w200/c414cDeQ9b6qLPLeKmiJuLDUREJ.jpg"),
        ("The Lion King",1994,"Animation",10,"https://image.tmdb.org/t/p/w200/2bXbqYdUdNVa8VIWXVfclP2ICtT.jpg"),
        ("Frozen",2013,"Animation",8,"https://image.tmdb.org/t/p/w200/kgwjIb2JDHRhNk13lmSxiClFjVk.jpg"),
        ("Toy Story",1995,"Animation",9,"https://image.tmdb.org/t/p/w200/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg"),
        ("The Avengers",2012,"Action",8,"https://image.tmdb.org/t/p/w200/RYMX2wcKCBAr24UyPD7xwmjaTn.jpg"),
        ("Iron Man",2008,"Action",8,"https://image.tmdb.org/t/p/w200/78lPtwv72eTNqFW9COBYI0dWDJa.jpg"),
        ("Spider-Man",2002,"Action",8,"https://image.tmdb.org/t/p/w200/gh4cZbhZxyTbgxQPxD0dOudNPTn.jpg"),
        ("Harry Potter 1",2001,"Fantasy",9,"https://image.tmdb.org/t/p/w200/wuMc08IPKEatf9rnMNXvIDxqP4W.jpg"),
        ("Harry Potter 2",2002,"Fantasy",8,"https://image.tmdb.org/t/p/w200/sdEOH0992YZ0QSxgXNIGLq1ToUi.jpg"),
        ("LOTR Fellowship",2001,"Fantasy",10,"https://image.tmdb.org/t/p/w200/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg"),
        ("LOTR Towers",2002,"Fantasy",10,"https://image.tmdb.org/t/p/w200/5VTN0pR8gcqV3EPUHHfMGnJYN9L.jpg"),
        ("LOTR Return",2003,"Fantasy",10,"https://image.tmdb.org/t/p/w200/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg"),
        ("Top Gun",1986,"Action",8,"https://image.tmdb.org/t/p/w200/bVq65huQ8vHDd1a4Z37QtuyEvpA.jpg"),
        ("Top Gun Maverick",2022,"Action",9,"https://image.tmdb.org/t/p/w200/62HCnUTziyWcpDaBO2i1DX17ljH.jpg"),
        ("Joker",2019,"Drama",9,"https://image.tmdb.org/t/p/w200/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg"),
        ("Shrek",2001,"Animation",8,"https://image.tmdb.org/t/p/w200/iB64vpL3dIObOtMZgX3RqdVdQDc.jpg"),
        ("Cars",2006,"Animation",7,"https://image.tmdb.org/t/p/w200/abW5AzHDaIK1n9C36VdAeOwORRA.jpg"),
        ("Up",2009,"Animation",9,"https://image.tmdb.org/t/p/w200/mFvoEwSfLqbcWwFsDjQebn9bzFe.jpg"),
        ("Finding Nemo",2003,"Animation",9,"https://image.tmdb.org/t/p/w200/eHuGQ10FUzK1mdOY69wF5pGgEf5.jpg"),
        ("Coco",2017,"Animation",10,"https://image.tmdb.org/t/p/w200/gGEsBPAijhVUFoiNpgZXqRVWJt2.jpg"),
        ("Moana",2016,"Animation",8,"https://image.tmdb.org/t/p/w200/4JeeQKzH5WfK3wM1TSt7YqTQ2h3.jpg")
        ]

        for m in movies:
            cur.execute(
                "INSERT INTO movies(title,year,genre,rating,image_url) VALUES(%s,%s,%s,%s,%s)", m
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
    page = int(request.args.get("page",1))
    size = int(request.args.get("size",10))
    search = request.args.get("search","")
    rating = request.args.get("rating","")
    sort = request.args.get("sort","title")

    allowed = ["title","rating","year"]
    if sort not in allowed:
        sort="title"

    offset = (page-1)*size

    conn = db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    sql = "SELECT * FROM movies WHERE title ILIKE %s"
    params = [f"%{search}%"]

    if rating:
        sql += " AND rating=%s"
        params.append(rating)

    sql += f" ORDER BY {sort} LIMIT %s OFFSET %s"
    params += [size,offset]

    cur.execute(sql,params)
    movies = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM movies")
    total = cur.fetchone()["count"]

    return jsonify({"movies":movies,"total":total})

# ---------- ADD ----------
@app.route("/movies",methods=["POST"])
def add_movie():
    d=request.json
    conn=db()
    cur=conn.cursor()
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
    conn=db()
    cur=conn.cursor()
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
    conn=db()
    cur=conn.cursor()
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