from flask.templating import render_template_string
from flask_app import app
from flask_app.models.user import User
from flask import render_template, flash, request, redirect, session
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/reset_password")
def reset_password():
    return render_template("reset.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    if User.validate(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "user_name": request.form["user_name"],
            "email": request.form["email"],
            "password": pw_hash
        }
        User.create_user(data)
        flash("Account created. Login!", "login")
        return redirect("/login")
    else:
        return redirect("/register")

@app.route("/user_login", methods=["POST"])
def user_login():
    data = {
        "email": request.form["email"]
    }
    users_in_db = User.all_users(data)
    if not users_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/login")
    if not bcrypt.check_password_hash(users_in_db.password, request.form["password"]):
        flash ("Invalid Email/Password", "login")
        return redirect("/login")
    session["user_id"] = users_in_db.id
    session["first_name"] = users_in_db.first_name
    print(session["first_name"])
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Must be logged in to view page")
        return redirect("/login")
    data= {
        "id": session["user_id"]
    }
    user = User.get_user_by_id(data)
    friends = User.get_friends(data)
    recent = User.get_recent_friend_wishes(data)
    user_recent = User.get_user_recent_wishes(data)
    # wish = Wish.show_wish_by_id(data)
    print(len(friends.friends))
    if len(friends.friends) < 1:
        no_friends = True 
    else:
        no_friends = False 
    return render_template("dashboard.html", user = user, friends=friends, recent=recent, user_recent=user_recent, no_friends = no_friends)

@app.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged Out!")
    return redirect("/login")
