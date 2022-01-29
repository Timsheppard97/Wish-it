from flask_app import app   
from flask import render_template, redirect, request,flash, session
from flask_app.models.wishlist import Wishlist
from flask_app.models.wish import Wish
from werkzeug.utils import secure_filename


@app.route("/create/wishlist", methods = ['POST'])
def create_wishlist():
    if Wishlist.validate_wishlist(request.form):
        if "user_id" not in session:
            flash("Must be logged in to view page")
            return redirect("/login")
        data = {
            "type" : request.form["type"],
            "name" : request.form["name"],
            "tag" : request.form["tag"],
            "color" : request.form["color"],
            "description" : request.form["description"],
            "user_id" : session["user_id"]
        }
        wishlist_id = Wishlist.create_wishlist(data)
        session["wishlist_id"] = wishlist_id
        return redirect ("/new_wish/"+str(session["user_id"]))
    else:
        return redirect("/create_wishlist")


@app.route("/userwishlist/<int:id>")
def usherwishlist_dashboard(id):
    if "user_id" not in session:
        flash("Must be logged in to view page")
        return redirect("/login")
    data = {
        "id": id,
    }
    all_wishlists = Wishlist.show_all_wishlists_by_user_id(data)
    wishes = Wish.show_wishes_by_userid(data)
    allwishes = True
    return render_template("userwishlist.html", all_wishlists = all_wishlists, wishes = wishes, allwishes=allwishes)


@app.route("/userwishlist/<int:id>/<int:wishlist_id>")
def view_wishes_in_wishlist(id, wishlist_id):
    if "user_id" not in session:
        flash("Must be logged in to view page")
        return redirect("/login")
    data = {
        "id": id,
        "wishlist_id": wishlist_id
    }
    all_wishlists = Wishlist.show_all_wishlists_by_user_id(data)
    wishlist = Wish.show_wishes_by_wishlistid(data)
    delete = True
    return render_template("userwishlist.html", wishlist = wishlist, all_wishlists = all_wishlists, delete=delete)


@app.route("/edit_wishlist")
def edit_wishlist():
    if "user_id" not in session:
        flash("Must be logged in to view page")
        return redirect("/login")
    return render_template("edit_wishlist.html")


@app.route("/create_wishlist")
def create_wishlist_page():
    if "user_id" not in session:
        flash("Must be logged in to view page")
        return redirect("/login")
    return render_template("create_wishlist.html")

@app.route("/delete_wishlist/<int:id>/<int:wishlist_id>")
def delete_wishlist(id, wishlist_id):
    data={
        "id": id,
        "wishlist_id": wishlist_id
    }
    Wishlist.delete_wishlist(data)
    return redirect("/userwishlist/"+str(session["user_id"]))

