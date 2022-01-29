from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import wish
from flask import flash

class Wishlist:
    def __init__( self , data ):
        self.id = data['id']
        self.type = data['type']
        self.name = data['name']
        self.tag = data['tag']
        self.color = data['color']
        self.status = data['status']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data["user_id"]
        self.wish = []

    @classmethod
    def create_wishlist(cls, data):
        query = "INSERT INTO wishlists (type, name, tag, color, description, user_id ) VALUES (%(type)s,%(name)s,%(tag)s,%(color)s,%(description)s, %(user_id)s);"
        return connectToMySQL("Wish_it").query_db( query , data )

    @classmethod
    def show_all_wishlists_by_user_id( cls, data ):
        query = "SELECT * FROM wishlists WHERE user_id = %(id)s"
        results = connectToMySQL("Wish_it").query_db(query,data)
        wishlists = []
        for wishlist in results:
            wishlists.append(cls(wishlist))
        return wishlists

    @classmethod
    def show_wishlist_with_wishes( cls , data ):
        query = "SELECT * FROM wishlists JOIN wishes ON wishlists.id = wishes.wishlist_id WHERE wishlists.id = %(wishlist_id)s;"
        results = connectToMySQL('Wish_it').query_db( query,data )
        wishlist = Wishlist(results[0])
        for database in results:
            wish_data = {
                "id" : database["wishes.id"],
                "name" : database["wishes.name"],
                "price" : database["price"],
                "url" : database["url"],
                "status" : database["status"],
                "description" : database["description"],
                "created_at" : database["wishes.created_at"],
                "updated_at" : database["wishes.updated_at"]
            }
            wishlist.wish.append(wish.Wish( wish_data ) )
        return wishlist

    @classmethod
    def delete_wish(cls,data):
        query = "DELETE FROM Wishes WHERE id = %(id)s"
        return connectToMySQL("wish_it").query_db( query, data )

    @classmethod
    def delete_wishlist(cls, data):
        query = "DELETE FROM wishlists WHERE id = %(wishlist_id)s"
        return connectToMySQL("wish_it").query_db( query, data )

    @staticmethod
    def validate_wishlist(wishlist):
        is_valid = True
        if len(wishlist['name'])<1:
            flash("Enter the name of the item you are wishing for!", "add_wishlist")
            is_valid = False
        if len(wishlist["type"])<1:
            flash("Enter the wishlist type", "add_wishlist")
            is_valid = False
        if len(wishlist["type"])<1:
            flash("Enter the tag!", "add_wishlist")
            is_valid = False
        if len(wishlist["description"])<1:
            flash("Enter wishlist description", "add_wishlist")
            is_valid = False
        return is_valid