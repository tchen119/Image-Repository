import sqlite3

# create the initial database
def make_datebase():
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # create table of images
    command = "CREATE TABLE images (image_id INTEGER PRIMARY KEY, filepath TEXT, user_id INTEGER, price FLOAT, quantity INTEGER);"
    db.execute(command)

    # create user table
    command = "CREATE TABLE users (user_id INTEGER PRIMARY KEY, username TEXT, balance INTEGER);"
    db.execute(command)

    db.commit()
    db.close()

# add user to the user table
def add_user(username, balance):
    db = sqlite3.connect("app.db")
    c = db.cursor()

    command = "SELECT count(*) FROM users;"
    for row in c.execute(command):
        user_id = row[0]

    command = "INSERT INTO users VALUES (%d, \"%s\", %d);" % (user_id, username, balance)
    c.execute(command)

    db.commit()
    db.close()

    return user_id

# add image to image table
def add_image(filepath, user_id, price, quantity):
    db = sqlite3.connect("app.db") 
    c = db.cursor()

    command = "SELECT count(*) FROM images;"
    for row in c.execute(command):
        image_id = row[0]

    command = "INSERT INTO images VALUES (%d, \"%s\", %d, %d, %d);" % (image_id, filepath, user_id, price, quantity)
    c.execute(command)

    db.commit()
    db.close()

    return image_id

# returns the price of an image
def get_image_price(image_id):
    db = sqlite3.connect("app.db")
    c = db.cursor()

    command = "SELECT price FROM images WHERE images.image_id = %d;" % (image_id) 
    for row in c.execute(command):
        price = row[0]

    db.commit()
    db.close()

    return price

# returns the quantity of an image
def get_image_quantity(image_id):
    db = sqlite3.connect("app.db")
    c = db.cursor()

    command = "SELECT quantity FROM images WHERE images.image_id = %d;" % (image_id) 
    for row in c.execute(command):
        quantity = row[0]

    db.commit()
    db.close()

    return quantity

# returns the filepath of an image
def get_image_filepath(image_id):
    db = sqlite3.connect("app.db")
    c = db.cursor()

    command = "SELECT filepath FROM images WHERE images.image_id = %d;" % (image_id) 
    for row in c.execute(command):
        filepath = row[0]

    db.commit()
    db.close()

    return filepath

# returns the entry that matches the user id and filepath
def get_inventory_quantity(user_id, filepath):
    db = sqlite3.connect("app.db")
    c = db.cursor()

    id = -1

    command = "SELECT image_id FROM images WHERE images.filepath = %s AND images.user_id = %d;" % (filepath, user_id) 
    for row in c.execute(command):
        id = row[0]

    db.commit()
    db.close()

    return id

# returns user balance
def get_user_balance(user_id):
    db = sqlite3.connect("app.db")
    c = db.cursor()

    command = "SELECT balance FROM users WHERE users.user_id = %d;" % (user_id) 
    for row in c.execute(command):
        balance = row[0]

    db.commit()
    db.close()

    return balance

# returns dictionary of images with price and quantity associated with the user
def get_images_from_user(user_id):
    db = sqlite3.connect("app.db")
    c = db.cursor()

    image_list = {}

    command = "SELECT * FROM images WHERE images.user_id = %d;" % (user_id)
    for row in c.execute(command):
        image = {}
        image['filepath'] = row[1]
        image['price'] = row[3]
        image['quantity'] = row[4]
        image_list[row[0]] = image

    db.commit()
    db.close()

    return image_list

# returns list of images in the marketplace, every other image besides user's
def get_marketplace_images(user_id):
    db = sqlite3.connect("app.db")
    c = db.cursor()

    image_list = {}

    command = "SELECT * FROM images WHERE images.user_id != %d;" % (user_id)
    for row in c.execute(command):
        image = {}
        image['filepath'] = row[1]
        image['price'] = row[3]
        image['quantity'] = row[4]
        image_list[row[0]] = image

    db.commit()
    db.close()

    return image_list

# changes the owner of the image 
def set_image_to_user(image_id, user_id):
    db = sqlite3.connect("app.db")
    c = db.cursor()

    command = "UPDATE images SET user_id = %d WHERE image_id = %d;" % (user_id, image_id)
    c.execute(command)

    db.commit()
    db.close()

# sets a user's balance to the input
def set_balance(user_id, balance):
    db = sqlite3.connect("app.db")
    c = db.cursor()

    command = "UPDATE users SET balance = %d WHERE user_id = %d;" % (balance, user_id)
    c.execute(command)

    db.commit()
    db.close()

# changes the quantity of the image 
def set_image_to_quantity(image_id, quantity):
    db = sqlite3.connect("app.db")
    c = db.cursor()

    command = "UPDATE images SET quantity = %d WHERE image_id = %d;" % (quantity, image_id)
    c.execute(command)

    db.commit()
    db.close()

# changes the price of the image 
def set_image_to_price(image_id, price):
    db = sqlite3.connect("app.db")
    c = db.cursor()

    command = "UPDATE images SET price = %d WHERE image_id = %d;" % (price, image_id)
    c.execute(command)

    db.commit()
    db.close()

if __name__ == "__main__":
    make_datebase()

    default_user_id = add_user('default', 100)
    user_id2 = add_user('Belts Seller', 100)
    user_id3 = add_user('Tshirt Seller', 100)

    add_image('/static/img/socks_5_pair.jpg', default_user_id, 5.00, 2)
    add_image('/static/img/belt_with_rings.jpg', user_id2, 10.00, 5)
    add_image('/static/img/grey_t-shirt.jpg', user_id3, 3.00, 10)