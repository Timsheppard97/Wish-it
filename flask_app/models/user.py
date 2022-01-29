from flask.helpers import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.wish import Wish
import re

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.user_name = data["user_name"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.user_picture = data["user_picture"]
        self.qr_code = data["qr_code"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.friends = []
        self.wishes = []

    @classmethod
    def get_all_users(cls, data):
        query = "SELECT * FROM users WHERE not id = %(id)s"
        user_db = connectToMySQL("wish_it").query_db(query, data)
        users = []
        user_friends = User.get_friends(data)
        friends = []
        if len(user_friends.friends) == 0:
            for user in user_db:
                if user['id'] not in friends:
                    users.append(User(user))
            # users.friends.append({'first_name':"",'last_name':""})
            return users
        for friend in user_friends.friends:
            friends.append(friend.id)
        for user in user_db:
            if user['id'] not in friends:
                users.append(User(user))
        return users

    @classmethod
    def get_friends(cls, data):
        query = "SELECT * FROM users LEFT JOIN friendships on users.id = friendships.user_id LEFT JOIN users as users2 on friendships.friend_id = users2.id WHERE users.id = %(id)s"
        user_db = connectToMySQL("wish_it").query_db(query, data)
        user = User(user_db[0])
        if not user_db[0]["friend_id"]:
            return user

        for result in user_db:
            friend_data = {
                "id": result["users2.id"],
                "user_name": result["users2.user_name"],
                "first_name": result["users2.first_name"],
                "last_name": result["users2.last_name"],
                "email": result["users2.email"],
                "password": result["users2.password"],
                "user_picture": result["users2.user_picture"],
                "qr_code": result["users2.qr_code"],
                "created_at": result["users2.created_at"],
                "updated_at": result["users2.updated_at"]
            }
            user.friends.append(User(friend_data))
        return user

    @classmethod
    def add_friend(cls, data):
        query = "INSERT INTO friendships (user_id, friend_id) VALUES (%(id)s, %(friend_id)s)"
        return connectToMySQL("wish_it").query_db(query, data)

    @classmethod
    def delete_friend(cls, data):
        query = "DELETE FROM friendships WHERE user_id=%(user_id)s AND friend_id = %(friend_id)s"
        return connectToMySQL("wish_it").query_db(query, data)

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users(first_name, last_name, user_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(user_name)s, %(email)s, %(password)s)"
        return connectToMySQL("wish_it").query_db(query, data)

    
    @classmethod
    def all_users(cls, data):
        query = "SELECT*FROM users WHERE email=%(email)s"
        user_db = connectToMySQL("wish_it").query_db(query, data)
        if len(user_db) < 1:
            return False
        return User(user_db[0])
    
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT*FROM users WHERE id=%(id)s"
        user_db = connectToMySQL("wish_it").query_db(query, data)
        return User(user_db[0])

    @classmethod
    def get_recent_friend_wishes(cls, data):
        query = "SELECT * FROM users LEFT JOIN friendships ON users.id=friendships.user_id LEFT JOIN users AS users2 ON users2.id=friendships.friend_id LEFT JOIN wishlists ON users2.id=wishlists.user_id LEFT JOIN wishes ON wishes.wishlist_id=wishlists.id WHERE users.id=%(id)s ORDER BY wishes.created_at DESC LIMIT 7"
        users_db = connectToMySQL("wish_it").query_db(query, data)
        main_user = User(users_db[0])
        if len(users_db) == 1:
            return User(users_db[0])
        for user in users_db:
            friend_data = {
                "id": user["users2.id"],
                "user_name": user["users2.user_name"],
                "first_name": user["users2.first_name"],
                "last_name": user["users2.last_name"],
                "email": user["users2.email"],
                "password": user["users2.password"],
                "user_picture": user["users2.user_picture"],
                "qr_code": user["users2.qr_code"],
                "created_at": user["users2.created_at"].strftime('%b %d, %Y'),
                "updated_at": user["users2.updated_at"],
            }
            wish_data = {
                "id" : user["wishes.id"],
                "name" : user["wishes.name"],
                "wish_image": user["wish_image"],
                "price" : user["price"],
                "url" : user["url"],
                "status" : user["status"],
                "description" : user["description"],
                "wishlist_id" : user["wishlist_id"],
                "created_at" : user["wishes.created_at"],
                "updated_at" : user["wishes.updated_at"]   
            }

            main_user.friends.append(User(friend_data))
            for friend in main_user.friends:
                friend.wishes.append(Wish(wish_data))
        return main_user

    @classmethod
    def get_user_recent_wishes(cls, data):
        query = "SELECT * FROM users LEFT JOIN wishlists on users.id=wishlists.user_id LEFT JOIN wishes ON wishlists.id=wishes.wishlist_id WHERE users.id=%(id)s ORDER BY wishes.created_at DESC LIMIT 4"
        user_db = connectToMySQL("wish_it").query_db(query, data)
        users = User(user_db[0])
        if len(user_db) == 1:
            return User(user_db[0])
        for user in user_db:
            wish_data = {
                "id" : user["wishes.id"],
                "name" : user["wishes.name"],
                "wish_image": user["wish_image"],
                "price" : user["price"],
                "url" : user["url"],
                "status" : user["status"],
                "description" : user["description"],
                "wishlist_id" : user["wishlist_id"],
                "created_at" : user["wishes.created_at"],
                "updated_at" : user["wishes.updated_at"] 
            }
            users.wishes.append(Wish(wish_data))
        return users



    @staticmethod
    def validate(user):
        email_regex = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')
        name_regex = re.compile(r'^[a-zA-Z ]+$')
        password_regex = re.compile(r'(?P<password>((?=\S*[A-Z])(?=\S*[a-z])(?=\S*\d)\S{8,}))')
        is_valid = True
        if len(user["first_name"]) < 2:
            flash("First name must be at least 2 characters", "register")
            is_valid = False
        elif not name_regex.match(user["first_name"]):
            flash("Letters only for first name", "register")
            is_valid = False
        if len(user["last_name"]) < 2:
            flash("Last name must be at least 2 characters", "register")
            is_valid = False
        elif not name_regex.match(user["last_name"]):
            flash("Letters only for last name", "register")
            is_valid = False
        if len(user["user_name"]) < 2:
            flash("Username must be at least 2 characters", "register")
        if not email_regex.match(user["email"]):
            flash("Invalid Email", "register")
            is_valid = False
        if not password_regex.match(user["password"]):
            flash("Password must include 8 characters, uppercase letter, lowercase letter, and number", "register")
            is_valid = False
        if (user["password"] == ""):
            flash("Enter password", "register")
            is_valid = False
        elif (user["password"] != user["confirm_password"]):
            flash("Passwords must match", "register")
            is_valid = False
        return is_valid
