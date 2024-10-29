from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
        )
    """
)
conn.commit()
conn.close()


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        query = f"SELECT username FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"Running query: {query}")

        try:
            cursor.execute(query)
            user_db = cursor.fetchone()
            if user_db:
                print(f"User found: {user_db[0]}")
                return render_template("logged.html", user=user_db[0])
            else:
                return render_template("login.html", error="Datos erroneos")
        except sqlite3.Error as e:
            print(f"Error: {e}")
            error = f"Error en la consulta: {e}"
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
        print(f"Running query: {query}")
        try:
            cursor.execute(query)
            conn.commit()

            return render_template("logged.html")
        except sqlite3.Error as e:
            print(f"Error: {e}")
            error = f"Error en la consulta: {e}"

    return render_template("register.html")
