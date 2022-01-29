
SELECT*FROM users

SELECT*FROM wishes
SELECT*FROM wishlists

SELECT * FROM wishes LEFT JOIN tags ON tags.wish_id = wishes.id LEFT JOIN wishlists ON tags.wishlist_id = wishlists.id WHERE wishes.id = 1

SELECT*FROM users JOIN wishlists ON users.id = user_id 
JOIN tags ON wishlist_id = wishlists.id JOIN wishes ON wish_id = wishlists.id WHERE users.id = 1 AND wishlist_id = 1

-- 
SELECT*FROM users JOIN wishlists ON users.id = user_id JOIN wishes ON wishes.wishlist_id WHERE wishlists.id = 2
LEFT JOIN wishes ON wishes.wishlist_id WHERE wishlists.id = 1
-- 


INSERT INTO wishlists (name, description, user_id) VALUES("2022", "party", 1)
INSERT INTO wishes (name, price, url, description, wishlist_id) VALUES("bob", 12,"fgcjtjyvty", "decrip", "1" )


