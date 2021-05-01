import os
from flask import Flask, render_template, request, flash, redirect
from db_tool import get_user_balance, get_image_filepath, get_inventory_quantity, get_images_from_user, get_image_price, get_image_quantity, get_marketplace_images, set_image_to_user, set_balance, set_image_to_quantity, add_image, remove_image
from werkzeug.utils import secure_filename

UPLOAD = 'static/img/'

app = Flask(__name__)
app.config['SECRET_KEY'] = "TH15 15 4 53CR3T K3Y"
app.config['UPLOAD'] = UPLOAD

@app.route('/', methods = ['GET', 'POST'])
def inventory():
    default_user_balance = get_user_balance(0)

    if request.method == 'POST':
        if 'id' in request.form: 
            id = int(request.form['id'])
        
            originalQuantity = get_image_quantity(id)
            imagePrice = get_image_price(id)
        
            sellQuantity = 1

            #update quantity if input is valid
            if (sellQuantity <= originalQuantity and originalQuantity >= 0):
                set_image_to_quantity(id, originalQuantity - sellQuantity)
                set_balance(0, default_user_balance + sellQuantity * imagePrice)
                #add sold items to the marketplace
                add_image(get_image_filepath(id), 1, get_image_price(id), sellQuantity) 
                #remove unneeded rows from images table
                if get_image_quantity(id) == 0:
                    remove_image(id)

        if 'file' in request.files:
            if 'price' not in request.form:
                flash('Please enter a price.')
            else:
                file = request.files['file']
                if request.form['price'] == "":
                    flash("Please enter a price.") 
                else:    
                    price = float(request.form['price'])

                    if file.filename == '':
                        flash('No selected file')
                    else:
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD'], filename))
                        add_image(UPLOAD + filename, 0, price, 1)

        default_user_balance = get_user_balance(0)
        inventory_from_default = get_images_from_user(0)
        return render_template('inventory.html', inventory = inventory_from_default, balance = default_user_balance)
    else:
        inventory_from_default = get_images_from_user(0)
        return render_template('inventory.html', inventory = inventory_from_default, balance = default_user_balance)

@app.route('/marketplace', methods = ['GET', 'POST'])
def marketplace():
    default_user_balance = get_user_balance(0)

    if request.method == 'POST':
        id = int(request.form['id'])
        originalQuantity = get_image_quantity(id)
        imagePrice = get_image_price(id)

        buyQuantity = 0
        #check for bad input
        if request.form['buyQuantity'] != "":
            buyQuantity = int(request.form['buyQuantity'])

        #update quantity if input is valid
        if (buyQuantity <= originalQuantity and originalQuantity >= 0 and imagePrice < default_user_balance):
            set_image_to_quantity(id, originalQuantity - buyQuantity)
            set_balance(0, default_user_balance - buyQuantity * imagePrice)
            #add bought items to inventory
            add_image(get_image_filepath(id), 0, get_image_price(id), buyQuantity)
            #remove image from user
            if get_image_quantity(id) == 0:
                remove_image(id)
        else:
            flash("Not enough money to purchase this item.")

        marketplace_items = get_marketplace_images(0)
        default_user_balance = get_user_balance(0)

        return render_template('marketplace.html', marketplace = marketplace_items, balance = default_user_balance)
    else:
        marketplace_items = get_marketplace_images(0)
        
        return render_template('marketplace.html', marketplace = marketplace_items, balance = default_user_balance)

if __name__ == '__main__':
    app.debug = True
    app.config["CACHE_TYPE"] = "null"
    app.run()