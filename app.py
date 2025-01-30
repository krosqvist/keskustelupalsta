import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import conversations

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_conversations = conversations.get_conversations()
    return render_template("index.html", conversations=all_conversations)

@app.route("/find_conversation")
def find_conversation():
    query = request.args.get("query")
    category = request.args.get("category")
    if query:
        params = [f"%{query}%"]
    else:
        params = ["%%"]
    if category:
        params.append(str(category))
    results = conversations.find_conversations(params)
    return render_template("find_conversation.html", query=query, category=category, results=results)

@app.route("/conversation/<int:conversation_id>")
def show_conversation(conversation_id):
    conversation = conversations.get_conversation(conversation_id)
    return render_template("show_conversation.html", conversation=conversation)

@app.route("/new_conversation")
def new_conversation():
    return render_template("new_conversation.html")

@app.route("/create_conversation", methods=["POST"])
def create_conversation():
    title = request.form["title"]
    category = request.form["category"]
    opening = request.form["opening"]
    user_id = session["user_id"]

    conversation_id = conversations.add_conversation(title, category, opening, user_id)
    return redirect("/conversation/" + str(conversation_id))

@app.route("/edit_conversation/<int:conversation_id>")
def edit_conversation(conversation_id):
    conversation = conversations.get_conversation(conversation_id)
    return render_template("edit_conversation.html", conversation=conversation)

@app.route("/update_conversation", methods=["POST"])
def update_conversation():
    conversation_id = request.form["conversation_id"]
    title = request.form["title"]
    category = request.form["category"]
    opening = request.form["opening"]

    conversations.update_conversation(conversation_id, title, category, opening)
    return redirect("/conversation/" + str(conversation_id))

@app.route("/delete_conversation/<int:conversation_id>", methods=["GET", "POST"])
def delete_conversation(conversation_id):
    if request.method == "GET":
        conversation = conversations.get_conversation(conversation_id)
        return render_template("delete_conversation.html", conversation=conversation)

    if request.method == "POST":
        if "delete" in request.form:
            conversations.delete_conversation(conversation_id)
            return redirect("/")
        else:
            return redirect("/conversation/" + str(conversation_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return "VIRHE: salasanat eivät ole samat"
        password_hash = generate_password_hash(password1)

        try:
            sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
            db.execute(sql, [username, password_hash])
        except sqlite3.IntegrityError:
            return "VIRHE: tunnus on jo varattu"

        return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        try:
            result = db.query(sql, [username])[0]
            user_id = result["id"]
            password_hash = result["password_hash"]
        except:
            return "VIRHE: Käyttäjätunnusta ei ole rekisteröity"
        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")
