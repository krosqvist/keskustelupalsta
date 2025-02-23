import sqlite3
import secrets
from flask import Flask
from flask import abort, redirect, render_template, request, session, make_response, flash
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import conversations
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"] or "csrf_token" not in request.form:
        abort(403)

@app.errorhandler(404)
def not_found(e):
    return redirect("/")

@app.errorhandler(403)
def not_found(e):
    return render_template("no_permission.html")

@app.route("/")
def index():
    all_conversations = conversations.get_conversations()
    return render_template("index.html", conversations=all_conversations)

@app.route("/find_conversation")
def find_conversation():
    classes = conversations.get_all_classes()
    query = request.args.get("query")
    if query:
        search = f"%{query}%"
    else:
        search = "%%"

    my_classes = []
    for entry in request.args.getlist("classes"):
        if entry:
            parts = entry.split(":")
            if parts[0] not in classes:
                abort(403)
            if parts[1] not in classes[parts[0]]:
                abort(403)
            my_classes.append((parts[0], parts[1]))

    results = conversations.find_conversations(search, my_classes)
    selected_classes = [f"{class_name}:{class_value}" for class_name, class_value in my_classes]
    return render_template("find_conversation.html", query=query, results=results, classes=classes, selected_classes=selected_classes)

@app.route("/find_user")
def find_user():
    query = request.args.get("query")
    if query:
        search = f"%{query}%"
    else:
        search = "%%"
    results = users.find_users(search)
    return render_template("find_user.html", query=query, results=results)

@app.route("/conversation/<int:conversation_id>")
def show_conversation(conversation_id):
    conversation = conversations.get_conversation(conversation_id)
    if not conversation:
        abort(404)
    classes = conversations.get_classes(conversation_id)
    comments = conversations.get_comments(conversation_id)
    return render_template("show_conversation.html", conversation=conversation, classes=classes, comments=comments)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    comments = users.get_comments(user_id)
    conversations = users.get_conversations(user_id)
    return render_template("show_user.html", user=user, conversations=conversations, comments=comments)

@app.route("/new_conversation")
def new_conversation():
    require_login()
    classes = conversations.get_all_classes()
    return render_template("new_conversation.html", classes=classes)

@app.route("/create_conversation", methods=["POST"])
def create_conversation():
    require_login()
    check_csrf()
    title = request.form["title"]
    if len(title) > 100:
        flash("Otsikko on liian pitkä!")
        return redirect("/new_conversation")
    if not title or title.startswith(" "):
        flash("Otsikon täytyy alkaa kirjaimella!")
        return redirect("/new_conversation")
    opening = request.form["opening"]
    if not opening or len(opening) > 5000:
        flash("Avaus on liian pitkä!")
        return redirect("/new_conversation")
    user_id = session["user_id"]

    file = request.files["image"]
    if file:
        if not file.filename.endswith(".jpg"):
            flash("Virheellinen tiedostomuoto!")
            return redirect("/new_conversation")

    image = file.read()
    if len(image) > 100 * 1024:
        flash("Liian suuri tiedosto!")
        return redirect("/new_conversation")

    all_classes = conversations.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            if parts[0] not in all_classes:
                abort(403)
            if parts[1] not in all_classes[parts[0]]:
                abort(403)
            classes.append((parts[0], parts[1]))

    conversation_id = conversations.add_conversation(title, opening, user_id, classes, image)
    return redirect("/conversation/" + str(conversation_id))

@app.route("/edit_conversation/<int:conversation_id>")
def edit_conversation(conversation_id):
    require_login()
    conversation = conversations.get_conversation(conversation_id)
    if not conversation:
        abort(404)
    if conversation["user_id"] != session["user_id"]:
        abort(403)

    all_classes = conversations.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in conversations.get_classes(conversation_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_conversation.html", conversation=conversation, classes=classes, all_classes=all_classes)

@app.route("/update_conversation", methods=["POST"])
def update_conversation():
    require_login()
    check_csrf()
    conversation_id = request.form["conversation_id"]
    conversation = conversations.get_conversation(conversation_id)
    if not conversation:
        abort(404)
    if conversation["user_id"] != session["user_id"]:
        abort(403)
    title = request.form["title"]
    if len(title) > 100:
        flash("Otsikko on liian pitkä!")
        return redirect("/edit_conversation/" + str(conversation_id))
    if not title or title.startswith(" "):
        flash("Otsikon täytyy alkaa kirjaimella!")
        return redirect("/edit_conversation/" + str(conversation_id))
    opening = request.form["opening"]
    if not opening or len(opening) > 5000:
        flash("Avaus on liian pitkä!")
        return redirect("/edit_conversation/" + str(conversation_id))

    file = request.files["image"]
    if file:
        if not file.filename.endswith(".jpg"):
            flash("Virheellinen tiedostomuoto!")
            return redirect("/edit_conversation/" + str(conversation_id))

        image = file.read()
        if len(image) > 100 * 1024:
            flash("Liian suuri tiedostokoko!")
            return redirect("/edit_conversation/" + str(conversation_id))
    else:
        image = conversation["image"]

    remove_image = request.form.get("delete_image")
    if remove_image == "1":
        image = None

    all_classes = conversations.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            if parts[0] not in all_classes:
                abort(403)
            if parts[1] not in all_classes[parts[0]]:
                abort(403)
            classes.append((parts[0], parts[1]))

    conversations.update_conversation(conversation_id, title, opening, classes, image)
    return redirect("/conversation/" + str(conversation_id))

@app.route("/delete_conversation/<int:conversation_id>", methods=["GET", "POST"])
def delete_conversation(conversation_id):
    require_login()
    conversation = conversations.get_conversation(conversation_id)
    if not conversation:
        abort(404)
    if conversation["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("delete_conversation.html", conversation=conversation)

    if request.method == "POST":
        check_csrf()
        if "delete" in request.form:
            conversations.delete_conversation(conversation_id)
            return redirect("/")
        else:
            return redirect("/conversation/" + str(conversation_id))

@app.route("/image/<int:conversation_id>")
def show_image(conversation_id):
    image = conversations.get_image(conversation_id)
    if not image:
        abort(404)
    response = make_response(image)
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/delete_comment/<int:comment_id>", methods=["POST"])
def delete_comment(comment_id):
    require_login()
    check_csrf()
    comment = conversations.check_comment(comment_id)
    conversation_id = request.form["conversation_id"]
    if comment["user_id"] != session["user_id"]:
        abort(403)
    if not comment:
        abort(404)
    conversations.delete_comment(comment_id)
    return redirect("/conversation/" + str(conversation_id))

@app.route("/create_comment", methods=["POST"])
def new_comment():
    require_login()
    check_csrf()
    comment = request.form["comment"]
    if not comment:
        abort(403)
    if len(comment) > 5000:
        flash("Kommentti on yli 5000 merkkiä!")
        return redirect("/conversation/" + str(conversation_id))
    conversation_id = request.form["conversation_id"]
    if not conversation_id:
        abort(403)
    user_id = session["user_id"]
    conversations.add_comment(comment, conversation_id, user_id)
    return redirect("/conversation/" + str(conversation_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    if not username or len(username) < 3 or len(username) > 20:
        flash("Käyttäjänimen pituus täytyy olla 3-20 merkkiä!")
        return redirect("/register")
    password1 = request.form["password1"]
    if not password1 or len(password1) < 3:
        flash("Salasanan täytyy olla vähintään 3 merkkiä!")
        return redirect("/register")
    password2 = request.form["password2"]
    if password1 != password2:
        flash("Salasanat eivät täsmää!")
        return redirect("/register")
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        flash("Käyttäjätunnus on jo käytössä!")
        return redirect("/register")

    return render_template("account.html", message="Tunnus luotu")

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
            flash("Käyttäjätunnusta ei ole rekisteröity!")
            return redirect("/login")
        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("Väärä tunnus tai salasana!")
            return redirect("/login")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
