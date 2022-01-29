from flask_app import app
from flask import request, session, render_template, redirect
from werkzeug.utils import secure_filename

@app.route("/")
def function():
    return render_template("index.html")
