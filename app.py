from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from os import getenv
from sqlalchemy import exc

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
        session["user_id"] = user.id
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
        try:
            sql = text("INSERT INTO decks (user_id, name) VALUES (:user_id, :name)")
            db.session.execute(sql, {"user_id": user_id, "name": deck_name})
            db.session.commit()
            print("Deck created successfully")
            return redirect("/user")
        except exc.SQLAlchemyError as e:
            print("Database error:", e)
            db.session.rollback()
            return "Internal Server Error", 500
    return render_template("create_deck.html")

@app.route("/user")
def user_home():
    user_decks = get_user_decks(session["user_id"])
    return render_template("user_home.html", user_decks=user_decks)

def get_user_decks(user_id):
    sql = text("SELECT id, name FROM decks WHERE user_id = :user_id")
    result = db.session.execute(sql, {"user_id": user_id})
    decks = result.fetchall()
    return decks

@app.route("/deck/<int:deck_id>/add_flashcard", methods=["GET", "POST"])
def add_flashcard(deck_id):
    if request.method == "POST":
        question = request.form["question"]
        answer = request.form["answer"]

        try:
            sql = text("INSERT INTO flashcards (deck_id, question, answer) VALUES (:deck_id, :question, :answer)")
            db.session.execute(sql, {"deck_id": deck_id, "question": question, "answer": answer})
            db.session.commit()
            return redirect(f"/deck/{deck_id}")
        except exc.SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return "Internal Server Error", 500
    else:
        return render_template("add_flashcard.html", deck_id=deck_id)

@app.route("/deck/<int:deck_id>")
def deck_home(deck_id):
    sql = text("SELECT question, answer FROM flashcards WHERE deck_id = :deck_id")
    result = db.session.execute(sql, {"deck_id": deck_id})
    flashcards = result.fetchall()
    return render_template("deck_home.html", flashcards=flashcards, deck_id=deck_id)

@app.route("/learn/<int:deck_id>")
def learn(deck_id):
    sql = text("SELECT id, question FROM flashcards WHERE deck_id = :deck_id AND level = 1 ORDER BY id LIMIT 1")
    result = db.session.execute(sql, {"deck_id": deck_id})
    card = result.fetchone()
    if card:
        session["current_deck_id"] = deck_id
        return redirect(url_for("show_question", card_id=card.id))
    else:
        return "No level 1 cards in deck", 400
    
@app.route("/card/<int:card_id>/question")
def show_question(card_id):
    sql = text("SELECT question FROM flashcards WHERE id = :card_id")
    result = db.session.execute(sql, {"card_id": card_id})
    card = result.fetchone()
    return render_template("show_question.html", card=card, card_id=card_id)

@app.route("/card/<int:card_id>/answer")
def show_answer(card_id):
    sql = text("SELECT question, answer FROM flashcards WHERE id = :card_id")
    result = db.session.execute(sql, {"card_id": card_id})
    card = result.fetchone()
    return render_template("show_answer.html", card=card, card_id=card_id)

@app.route("/card/<int:card_id>/good")
def increase_card_level(card_id):
    try:
        sql = text("UPDATE flashcards SET level = level + 1 WHERE id = :card_id")
        db.session.execute(sql, {"card_id": card_id})
        db.session.commit()

        next_card_sql = text("SELECT id FROM flashcards WHERE deck_id = :deck_id AND level = 1 AND id > :card_id ORDER BY id ASC LIMIT 1")
        next_card_result = db.session.execute(next_card_sql, {"deck_id": session["current_deck_id"], "card_id": card_id})
        next_card = next_card_result.fetchone()

        if next_card:
            return redirect(url_for("show_question", card_id=next_card.id))
        else:
            return redirect(url_for("deck_home", deck_id=session["current_deck_id"]))
    except exc.SQLAlchemy as e:
        print(e)
        db.session.rollback()
        return "Internal Server Error", 500
    
@app.route("/card/<int:card_id>/again")
def show_question_again(card_id):
    return redirect(url_for("show_question", card_id=card_id))