from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector, os

app = Flask(__name__)
CORS(app)

def db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )

@app.route("/")
def home():
    return "Movie API running"

# READ with paging/search/sort
@app.route("/movies")
def get_movies():
    page = int(request.args.get("page",1))
    size = int(request.args.get("size",10))
    search = request.args.get("search","")
    sort = request.args.get("sort","title")

    offset = (page-1)*size

    conn=db();cur=conn.cursor(dictionary=True)

    cur.execute(f"""
        SELECT * FROM movies
        WHERE title LIKE %s
        ORDER BY {sort}
        LIMIT %s OFFSET %s
    """,(f"%{search}%",size,offset))

    movies=cur.fetchall()

    cur.execute("SELECT COUNT(*) total FROM movies")
    total=cur.fetchone()["total"]

    return jsonify({"movies":movies,"total":total})

# CREATE
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

# UPDATE
@app.route("/movies/<int:id>",methods=["PUT"])
def edit_movie(id):
    d=request.json
    conn=db();cur=conn.cursor()
    cur.execute("""
        UPDATE movies SET title=%s,year=%s,genre=%s,rating=%s,image_url=%s
        WHERE id=%s
    """,(d["title"],d["year"],d["genre"],d["rating"],d["image_url"],id))
    conn.commit()
    return {"msg":"updated"}

# DELETE
@app.route("/movies/<int:id>",methods=["DELETE"])
def delete_movie(id):
    conn=db();cur=conn.cursor()
    cur.execute("DELETE FROM movies WHERE id=%s",(id,))
    conn.commit()
    return {"msg":"deleted"}

# STATS
@app.route("/stats")
def stats():
    conn=db();cur=conn.cursor(dictionary=True)
    cur.execute("""
        SELECT COUNT(*) total,
               AVG(rating) avg_rating,
               COUNT(DISTINCT genre) genres
        FROM movies
    """)
    return jsonify(cur.fetchone())

app.run(host="0.0.0.0",port=5000)