from flask import Flask, render_template, request, flash, redirect, url_for, session
from .models import User, todays_recent_posts

app = Flask(__name__)

@app.route('/')
def index():
    posts = todays_recent_posts(5)
    return render_template("index.html", posts=posts)

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User(username)
        if not user.register(password):
            flash("A user with that username already exists.")
        else:
            flash("Successfully registered.")
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User(username)
        if not user.verify_password(password):
            flash("Invalid login.")
        else:
            flash("Successfully logged in.")
            session["username"] = user.username
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/add_post", methods=["POST"])
def add_post():
    title = request.form["title"]
    tags = request.form["tags"]
    text = request.form["text"]

    user = User(session["username"])

    if not title or not tags or not text:
        flash("You must give your post a title, tags, and a text body.")
    else:
        user.add_post(title, tags, text)

    return redirect(url_for("index"))


@app.route("/like_post/<post_id>")
def like_post(post_id):
    username = session.get("username")

    if not username:
        flash("You must be logged in to like a post.")
        return redirect(url_for("login"))

    user = User(username)
    user.like_post(post_id)
    flash("Liked post.")
    return redirect(request.referrer)


@app.route("/profile/<username>")
def profile(username):
    return "TODO"


@app.route("/logout")
def logout():
    return "TODO"