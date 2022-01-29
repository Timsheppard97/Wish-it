from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.wishlist import Wishlist
from flask_app.models.wish import Wish
from werkzeug.utils import secure_filename
import os
import shutil

@app.route("/new_wish/<int:id>")
def new_wish(id):
    if "user_id" not in session:
        flash("Must be logged in to view page")
        return redirect("/login")
    data = {
        "id": id
    }
    wishlists = Wishlist.show_all_wishlists_by_user_id(data)
    return render_template("add_wish.html", wishlists = wishlists)


@app.route("/createwish", methods = ['POST'])
def create_wish():
    if "user_id" not in session:
        flash("Must be logged in to view page")
        return redirect("/login")
    if Wish.validate_wish(request.form):
        pic = request.files["wish_image"]
        if pic.filename == "":
            flash("Choose image", "add")
            return redirect(f"/new_wish/{session['user_id']}")
        
        pic = request.files["wish_image"]
        filename = secure_filename(pic.filename)
        print("Pic filename:" +str(filename))
        save_path = "flask_app/static/wish_imgs"
        completePath = os.path.join(save_path, filename)
        pic.save(completePath)
        
        data = {
            "name" : request.form["name"],
            "price" : request.form["price"],
            "url" : request.form["url"],
            "description" : request.form["description"],
            "wish_image" : filename, 
            "wishlist_id" : request.form['wishlist_id']
        }
        Wish.create_wish(data)
        return redirect (f"/userwishlist/{session['user_id']}/{data['wishlist_id']}")
    else:
        return redirect(f"/new_wish/{session['user_id']}")


@app.route("/edit/<int:id>")
def make_edit_wish(id):
    if "user_id" not in session:
        flash("Must be logged in to view page")
        return redirect("/login")
    data = {
        "id": session["user_id"],
        "wish_id":id
    }
    wish = Wish.show_wish_by_id(data)
    wishlists = Wishlist.show_all_wishlists_by_user_id(data)
    return render_template("edit_wish.html",wish = wish, wishlists=wishlists )

@app.route("/edit_wish/<int:id>", methods = ['POST'])
def save_edit_wish(id):
    if "user_id" not in session:
        flash("Must be logged in to view page")
        return redirect("/login")
    if Wish.validate_wish(request.form):
        pic = request.files["wish_image"]
        if pic.filename == "":
            flash("Choose image", "add")
            return redirect(f"/new_wish/{session['user_id']}")
        
        pic = request.files["wish_image"]
        filename = secure_filename(pic.filename)
        print("Pic filename:" +str(filename))
        save_path = "flask_app/static/wish_imgs"
        completePath = os.path.join(save_path, filename)
        pic.save(completePath)
        
        data = {
            "id":id,
            "name": request.form["name"],
            "description": request.form["description"],
            "price": request.form["price"],
            "url" : request.form["url"],
            "wish_image": filename,
            "wishlist_id":request.form["wishlist_id"],
        }
        Wish.edit_wish(data)
        flash("Wish updated!", "update")
        return redirect(f"/userwishlist/{session['user_id']}")
    else:
        return redirect(f"edit/{id}")


@app.route("/insert_wish/tags", methods = ['POST'])
def insert_tags_for_wish ():
    if "user_id" not in session:
        flash("Must be logged in to view page")
        return redirect("/login")
    data = {
        "wishlist_id" : request.form ["wishlist_id"],
        "wish_id" : request.form ["wish_id"],
    }
    Wish.insert_tags_for_wish(data)
    return redirect(f"/wishlist/{request.form ['wish_id']}")


@app.route("/view/<int:wish_id>")
def view_wish(wish_id):
    data={
        "wish_id":wish_id,
    }
    wish = Wish.show_wish_by_id(data)
    return render_template("view.html", wish=wish)


@app.route("/delete/<int:id>")
def delete_wish(id):
    if "user_id" not in session:
        flash("Must be logged in to view page!")
        return redirect("/login")
    data = {
        "id" : id
    }
    Wish.delete_wish(data)
    return redirect (f"/userwishlist/{session['user_id']}")
