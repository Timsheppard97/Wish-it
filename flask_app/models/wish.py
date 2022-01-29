from flask.helpers import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import wishlist

class Wish:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.price = data['price']
        self.url = data['url']
        self.status = data['status']
        self.description = data['description']
        self.wish_image = data['wish_image']
        self.wishlist_id = data['wishlist_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_wish(cls, data):
        query = "INSERT INTO wishes (name, price, url, description, wish_image, wishlist_id) VALUES (%(name)s,%(price)s,%(url)s,%(description)s,%(wish_image)s,%(wishlist_id)s);"
        return connectToMySQL("Wish_it").query_db( query , data )

    @classmethod
    def edit_wish(cls,data):
        query = "UPDATE wishes SET name=%(name)s,price=%(price)s,url=%(url)s, description=%(description)s,wish_image=%(wish_image)s,wishlist_id=%(wishlist_id)s WHERE id = %(id)s"
        return connectToMySQL("wish_it").query_db( query, data )

    @classmethod
    def show_wish(cls):
        query = "SELECT * FROM wishes"
        results = connectToMySQL("Wish_it").query_db(query)
        wishes = []
        for wish in results:
            wishes.append(cls(wish))
        return wishes

    @classmethod
    def show_wishes_by_userid(cls,data):
        query = "SELECT * FROM users JOIN wishlists ON wishlists.user_id = users.id JOIN wishes on wishes.wishlist_id = wishlists.id WHERE users.id = %(id)s ORDER BY wishes.updated_at DESC"
        results_db = connectToMySQL("Wish_it").query_db(query,data)
        wishes = []
        for result in results_db:
            wish_data = {
                "id" : result["wishes.id"],
                "name" : result["wishes.name"],
                "wish_image": result["wish_image"],
                "price" : result["price"],
                "url" : result["url"],
                "status" : result["status"],
                "description" : result["description"],
                "wishlist_id" : result["wishlist_id"],
                "created_at" : result["wishes.created_at"],
                "updated_at" : result["wishes.updated_at"]   
            }
            wishes.append(Wish(wish_data))
        return wishes

    @classmethod
    def show_wish_by_id(cls,data):
        query = "SELECT * FROM wishes WHERE id = %(wish_id)s"
        results = connectToMySQL("Wish_it").query_db(query,data)
        return results[0]

    @classmethod
    def show_wishes_by_wishlistid(cls,data):
        query = "SELECT * FROM users JOIN wishlists ON wishlists.user_id = users.id JOIN wishes on wishes.wishlist_id = wishlists.id WHERE wishlists.id = %(wishlist_id)s"
        results_db = connectToMySQL("Wish_it").query_db(query,data)
        if not results_db:
            wishlist_id = False
            return wishlist_id
        wishlist_id = wishlist.Wishlist(results_db[0])
        for result in results_db:   
            wish_data = {
                "id" : result["wishes.id"],
                "name" : result["wishes.name"],
                "wish_image": result["wish_image"],
                "price" : result["price"],
                "url" : result["url"],
                "status" : result["status"],
                "description" : result["description"],
                "wishlist_id" : result["wishlist_id"],
                "created_at" : result["wishes.created_at"],
                "updated_at" : result["wishes.updated_at"]   
            }
            wishlist_id.wish.append(Wish(wish_data))
        return wishlist_id
        
    @classmethod
    def insert_tags_for_wish(cls,data):
        query  = "INSERT INTO tags (wishlist_id,wish_id) VALUES (%(wishlist_id)s,%(wish_id)s)"
        return connectToMySQL("Wish_it").query_db( query , data )


    @classmethod
    def delete_wish(cls,data):
        query = "DELETE FROM Wishes WHERE wishes.id = %(id)s"
        return connectToMySQL("wish_it").query_db( query, data )

    @staticmethod
    def validate_wish(wish):
        is_valid = True
        if len(wish['name'])<1:
            flash("Enter the name of the item you are wishing for!", "add")
            is_valid = False
        if len(wish['price'])<0:
            flash("The price of the item must be greater than 0!", "add")
            is_valid = False       
        if len(wish['url'])<1:
            flash("Please enter a valid url!", "add")
            is_valid = False 
        if len(wish['description'])<2:
            flash("Please enter a wish note!", "add")
            is_valid = False
        return is_valid

    @classmethod
    def view(cls, data):
        query = "SELECT*FROM wishes WHERE id=%(id)s"
        results = connectToMySQL('Wish_it').query_db(query , data)
        return results[0]
