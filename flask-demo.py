from flask import Flask, render_template, redirect, url_for, request
import sqlite3
import os
# from flask_mysqldb import MySQL

app = Flask(__name__)

# mysql = MySQL(app)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'MyDB'

def createDatabase():
    conn = sqlite3.connect("movieDB.db")
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS MOVIES(
                    ID INTEGER,
                    MOVIE TEXT,
                    YEAROFRELEASE TEXT,
                    GENRE TEXT,
                    PRIMARY KEY (ID)
                );
                """)

    cur.execute("""
                CREATE TABLE IF NOT EXISTS CAST(
                    ID INTEGER,
                    ACTOR TEXT,
                    ACTRESS TEXT,
                    DIRECTOR TEXT,
                    BOX_OFFICE INTEGER,
                    RATING INTEGER,
                    PRIMARY KEY (ID),
                    FOREIGN KEY (ID) REFERENCES MOVIES(ID)
                );
                """)
    conn.commit()


@app.route("/", methods = ['POST', 'GET'])
def home():
    conn = sqlite3.connect("movieDB.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM MOVIES")
    movieColumns = [description[0] for description in cur.description]
    movieData = cur.fetchall()

    cur.execute("SELECT * FROM CAST")
    castColumns = [description[0] for description in cur.description]
    castData = cur.fetchall()

    cur.close()

    return render_template("index.html", content = {"movieColumns" : movieColumns, "movieData" : movieData, "castColumns" : castColumns, "castData" : castData})


@app.route('/insert', methods = ['POST', 'GET'])
def insert():
    if request.method == 'POST':
        try:
            conn = sqlite3.connect("movieDB.db")
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO MOVIES(MOVIE, YEAROFRELEASE, GENRE) VALUES(?, ?, ?)",
                (
                    request.form.get("movie"), 
                    request.form.get("yearofrelease"),
                    request.form.get("genre")
                ),
            )
            cur.execute(
                "INSERT INTO CAST(ACTOR, ACTRESS, DIRECTOR, BOX_OFFICE, RATING) VALUES(?, ?, ?, ?, ?)",
                (
                    request.form.get("actor"),
                    request.form.get("actress"),
                    request.form.get("director"),
                    request.form.get("box_office"),
                    request.form.get("rating")
                )
            )
            
            cur.close()
            conn.commit()

            return redirect(url_for("insert"))
        except sqlite3.Error  as e:
            print(e)
            return e

    return render_template("insert.html")
    
if __name__ == "__main__":
    if not os.path.exists("movieDB.db"):
        createDatabase()
    app.run(debug=True)
