from flask_app import app
from flask_app.controllers import routes, users, wishlists, wishes, friends

if __name__ == "__main__":
    app.run(debug=True)
