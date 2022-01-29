from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User

@app.route("/friends/<int:id>")
def friends(id):
    data = {
        "id": id
    }
    in_session_user= User.get_friends(data)
    users = User.get_all_users(data)
    return render_template("friends.html", users=users, in_session_user=in_session_user)

@app.route("/add_friend/<int:id>", methods=["POST"])
def add_friend(id):
    data = {
        "id":id,
        "friend_id":request.form["add_friend"]
    }
    User.add_friend(data)
    return redirect(f"/friends/{id}")

@app.route("/delete_friend/<int:friend_id>")
def delete_friend(friend_id):
    data = {
        "friend_id":friend_id,
        "user_id": session["user_id"]
    }
    User.delete_friend(data)
    return redirect(f"/friends/{data['user_id']}")


