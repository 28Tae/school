import os


# Hint1: please use db_file instead of typing the file name
# this will help you to avoid potential errors
curr_dir = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(curr_dir, 'survey.db')


# Hint2: You may use the following variables for your convenience
STORES = [
    'Jap Food', 'Mixed Vege', 'Western Delight',
    'Chicken Rice', 'K Food', 'Local Delight',
    'Drink Store'
]

SEC3_CLASSES = ('3A1', '3A2', '3A3')
SEC4_CLASSES = ('4A1', '4A2', '4A3')

# Your code here

import sqlite3
from random import choice
from flask import request, redirect, url_for, Flask, render_template, flash

def execute_db(query: str, tup: tuple = None):
    """Helper function to execute a SELECT/commitable statement in the db, makes life simpler"""
    conn = sqlite3.connect(db_file)

    if query.strip().startswith("SELECT"):
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
@app.route("/index")
def index():
    # Finds out stores to flesh on dropdown for Task 2.2
    stores = execute_db(
        """SELECT DISTINCT Fav_Store FROM Survey ORDER BY Fav_Store"""
    )
    stores = [i[0] for i in stores]
    return render_template("index.html", stores=stores)


@app.route("/form", methods=["GET", "POST"])
@app.route("/form/<cls>")
def form(cls='4A3'):
    # Accepts /form/<cls> or form/ which defaults to 4I2
    # Parses uppercase and checks if valid
    if request.method == "POST":
        cls = request.form["cls"]
    cls = cls.upper()
    if not(cls in SEC3_CLASSES or cls in SEC4_CLASSES):
        return "That's not valid bro"
    
    data = execute_db(
        """SELECT Fav_Subj, Count(*) FROM Survey
        WHERE Class = ?
        GROUP BY Fav_Subj
        ORDER BY Count(*) DESC""",
        (cls,)
    )
    return render_template(
        "result.html",
        cls = cls,
        data = data
    )

@app.route("/thanks", methods=["POST"])
def thanks():
    # Strictly by POST from index dropdown
    store = request.form["store"]
    sec_3s = execute_db(
        """SELECT Class, Name FROM Survey
        WHERE Fav_Store = ?
        AND Class LIKE '3A%'""",
        (store, )
    )
    sec_4s = execute_db(
        """SELECT Class, Name FROM Survey
        WHERE Fav_Store = ?
        AND Class LIKE '4A%'""",
        (store, )
    )

    # Randomly pick from a sec 3 or 4
    return render_template(
        "store.html",
        store=store,
        s3=choice(sec_3s),
        s4=choice(sec_4s),
    )

if __name__ == "__main__":
    app.run(debug=True)