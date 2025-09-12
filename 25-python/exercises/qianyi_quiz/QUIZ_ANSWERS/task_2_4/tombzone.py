import sqlite3
from os import path
from flask import request, render_template, redirect, url_for, Flask

# You can just do "tombzone.db"
# But this is to ensure the correct directory is used
base_path = lambda filename: path.join(path.dirname(path.abspath(__file__)), filename)
DB_FILE = base_path("tombzone.db")

def exec_query(query: str, tup: tuple=None):
    """Helper function to execute a query on DB file"""
    conn = sqlite3.connect(DB_FILE)
    if query.strip().upper().startswith("SELECT"):
        cursor = conn.execute(query, tup) if tup else conn.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    else:
        if tup:
            conn.execute(query, tup)
        else:
            conn.execute(query)
        conn.commit()
        conn.close()

app = Flask(__name__)

@app.route("/")
def index():
    # Not necessary, albeit customary, to implement /index
    return redirect(url_for("search"))

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        games = exec_query("SELECT game_name FROM Game ORDER BY game_name")
        return render_template("search.html", games=games)

    game = request.form["game"]

    # The query can be easily derived from Task 2.3
    query = """
    SELECT p.name, p.hp, p.gender, e.timestamp,
    ROUND((e.score*1.00)/g.max_score, 2) AS "score_percentage"
    FROM Game g
    INNER JOIN Entry e ON e.game_id = g.game_id
    INNER JOIN Player p ON p.player_id = e.player_id
    WHERE game_name = ?
    ORDER BY e.score DESC, e.timestamp ASC
    """
    data = exec_query(query, (game,))
    return render_template(
        "results.html",
        data=data,
        game=game
    )

@app.route("/add", methods=["GET", "POST"])
def add():
    def unpack() -> tuple:
        return (
            exec_query("SELECT game_name FROM Game ORDER BY game_name"),
            exec_query("SELECT player_id FROM Player ORDER BY player_id"),
        )
    
    if request.method == "GET":
        games, ids = unpack()
        return render_template("add.html", games=games, ids=ids)
    
    game_name, player_id, score = request.form["game_name"], request.form["player_id"], request.form["score"]

    # Resend form with user error, if score is NOT a non-negative integer
    try:
        score = int(score)
        if score < 0:
            raise ValueError
    except ValueError:
        games, ids = unpack()
        return render_template("add.html", games=games, ids=ids, error="Score must be non-negative!")
    
    # Retrieve game_id for entry insertion
    game_id = exec_query(
        "SELECT game_id FROM Game WHERE game_name = ?", 
        (game_name,)
    )[0][0]

    # Insert data
    # Take note of CURRENT_TIMESTAMP
    exec_query(
        """INSERT OR IGNORE INTO Entry (game_id, player_id, score, timestamp)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)""",
        (game_id, player_id, score)
    )

    # Retrieve name, gender, timestamp
    player_name, gender, timestamp = exec_query(
        "SELECT name, gender, CURRENT_TIMESTAMP FROM Player WHERE player_id = ?",
        (player_id,)
    )[0]

    return render_template(
        "added.html",
        player_name=player_name,
        gender=gender,
        game_name=game_name,
        score=score,
        timestamp=timestamp,
    )
        

if __name__ == "__main__":
    app.run(debug=True)