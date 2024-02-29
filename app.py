from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from os import getenv

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = text("SELECT  id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user and check_password_hash(user.password, password):
        session["username"] = username
        return redirect("/user")
    else:
        return redirect("/login")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_exists = db.session.execute(text("SELECT * FROM users WHERE username=:username"), {"username": username}).fetchone()
        if user_exists:
            return render_template("register.html", error="Username already exists")
        hash_value = generate_password_hash(password)
        db.session.execute(text("INSERT INTO users (username, password) VALUES (:username, :hash_value)"), {"username": username, "hash_value": hash_value})
        db.session.commit()
        return redirect("/")
    else:
        return render_template("register.html")
@app.route("/create_deck", methods=["GET", "POST"])
def create_deck():
    if request.method == "POST":
        deck_name = request.form["name"]
        user_id = session.get("user_id")
        if not deck_name:
            return "Deck name is required", 400
        sql = text("INSERT INTO decks (user_id, name) VALUES (:user_id, :name)")
        db.session.execute(sql, {"user_id": user_id, "name": deck_name})
        db.session.commit()
        return redirect("/")

@app.route("/user")
def user_home():
    return render_template("user_home.html")



