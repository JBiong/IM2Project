from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from users import create_user,authenticate_user,get_users
from orders import add_to_cart, edit_cart, view_cart, delete_cart_item  # Import the modified functions
from database import set_mysql, get_cursor, get_connection
from dotenv import load_dotenv

import os

load_dotenv()

app = Flask(__name__, template_folder=os.path.abspath('template'))

# Required
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
# Extra configs, optional but mandatory for this project:
app.config["MYSQL_CURSORCLASS"] = os.getenv("MYSQL_CURSORCLASS")
app.config["MYSQL_AUTOCOMMIT"] = True if os.getenv("MYSQL_AUTOCOMMIT") == "true" else False

mysql = MySQL(app)
set_mysql(mysql)

@app.route("/")
def home():
     return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        user = authenticate_user(data["email"], data["pass"])

        if user is not None:
            # Authentication successful
             response_data = {"id": user, "redirect_url": url_for('dashboard')}
             return jsonify(response_data), 200
        else:
            # Authentication failed
            return jsonify({"error": "Authentication failed"}), 401

    else:
        users = get_users()
        return jsonify(users)

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        data = request.get_json()
        user_id = create_user(data["name"], data["age"], data["email"], data["password"])
        return jsonify({"id": user_id})
    else:
        users = get_users()
        return jsonify(users)

    return render_template("login.html")

@app.route("/signup/<int:id>", methods=["GET"])
def user(id):
        user = get_users(id)
        return jsonify(user)
    

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route('/products', methods=['GET'])
def get_all_products():
    # Use flask_mysqldb to execute the SQL query
    cursor = get_cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()

    # Convert the products to a JSON format and return as a response
    product_list = [
        {
            'id': product['id'],
            'category': product['category'],
            'name': product['product_name'],
            'price': float(product['price']),  # Convert Decimal to float for JSON serialization
            'image_name': product['image_name']
        }
        for product in products
    ]

    return render_template("index.html")

@app.route('/add_to_cart_item', methods=['POST'])
def add_to_cart_routes():
    data = request.get_json()

    items = data.get('items', [])
    for item in items:
        product_id = item.get('product_id')
        size = item.get('size')
        quantity = item.get('quantity')

        if product_id and size and quantity:
            add_to_cart(product_id, size, quantity)

    # Fetch all orders from the database after the update
    orders = view_cart()
    total_amount = sum(order['price'] * order['quantity'] for order in orders)

    return jsonify({'orders': orders, 'total_amount': total_amount})

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart_route():

    total_products = 30  # Assuming you have 30 products

    # Fetch all orders and total amount from the database
    orders = view_cart()  # Use the view_cart function

    # Calculate the total amount
    total_amount = sum(order['price'] * order['quantity'] for order in orders)

    for dress_number in range(1, total_products + 1):
        product_id = request.form.get(f'product_id{dress_number}')
        size = request.form.get(f'size{dress_number}', '')


        # Check if the product is selected
        if not product_id:
            continue

        try:
            product_id = int(product_id)
        except ValueError:
            return redirect(url_for('index'))

        quantity = request.form.get(f'quantity{dress_number}', 0)

        try:
            quantity = int(quantity)
        except ValueError:
            return redirect(url_for('index'))

        if quantity > 0:
            # Check if the product is already in the cart
            cursor = get_cursor()
            cursor.execute("SELECT id FROM cart_items WHERE product_id = %s AND size = %s", (product_id, size))
            existing_cart_item = cursor.fetchone()

            if existing_cart_item:
                # Product already in the cart, update the quantity
                cursor.execute("UPDATE cart_items SET quantity = quantity + %s WHERE id = %s", (quantity, existing_cart_item['id']))
            else:
                # Product not in the cart, insert a new entry
                cursor.execute("INSERT INTO cart_items (product_id, size, quantity) VALUES (%s, %s, %s)", (product_id, size, quantity))
                cursor.close()
                
    # Check if the client accepts HTML
    if 'text/html' in request.accept_mimetypes:
        return render_template('orderlist.html', orders=orders, total_amount=total_amount)
    else:
        # Return a JSON response
        return jsonify({'orders': orders, 'total_amount': total_amount})

@app.route('/edit_cart', methods=['GET', 'POST'])
def edit_cart_route():

    if request.method == 'POST':
        # Initialize cursor before using it
        cursor = get_cursor()

        # Handle the form submission to update cart items
        for item_id, new_value in request.form.items():
            # Each form field is an item_id_quantity or item_id_size, and the corresponding value is the new quantity or size

            try:
                item_id, field = item_id.split('_')
                item_id = int(item_id)
            except ValueError:
                # Handle invalid input
                return redirect(url_for('edit_cart_route'))

            if field == 'delete' and new_value == '1':
                # Use the stored procedure for deletion
                delete_cart_item(item_id)

            elif field == 'quantity':
                # Handle quantity updates using POST method

                # Get the updated quantity from the form
                new_quantity = request.form.get(f'{item_id}_quantity', 0)

                try:
                    new_quantity = int(new_quantity)
                except ValueError:
                    # Handle invalid input
                    return redirect(url_for('edit_cart_route'))

                cursor.execute("UPDATE cart_items SET quantity = %s WHERE id = %s", (new_quantity, item_id))
                cursor.execute("UPDATE orders SET quantity = %s WHERE id = %s", (new_quantity, item_id))

            elif field == 'size':
                # Handle size updates using POST method

                # Get the updated size from the form
                new_size = request.form.get(f'{item_id}_size', '')
                cursor.execute("UPDATE cart_items SET size = %s WHERE id = %s", (new_size, item_id))
                cursor.execute("UPDATE orders SET size = %s WHERE id = %s", (new_size, item_id))

        # Commit changes to the database
        get_connection().commit()
        cursor.close()

    # Fetch all cart items from the database
    cursor = get_cursor()
    cursor.execute("SELECT cart_items.id, cart_items.product_id, cart_items.size, cart_items.quantity, "
                   "products.product_name, products.price, products.image_name "
                   "FROM cart_items JOIN products ON cart_items.product_id = products.id")
    cart_items = cursor.fetchall()
    cursor.close()

    # Check if the client accepts HTML
    if 'text/html' in request.accept_mimetypes:
        return render_template('edit_cart.html', cart_items=cart_items)
    else:
        # Return a JSON response
        return jsonify({'cart_items': cart_items})

@app.route('/edit_cart_item', methods=['POST'])
def edit_cart_routes():
    data = request.get_json()

    items = data.get('items', [])
    for item in items:
        item_id = item.get('item_id')
        quantity = item.get('quantity')
        size = item.get('size')

        if item_id:
            if 'delete' in item and item['delete']:
                delete_cart_item(item_id)
            else:
                if quantity:
                    # Update quantity in cart_items table
                    cursor = get_cursor()
                    cursor.execute("UPDATE cart_items SET quantity = %s WHERE id = %s", (quantity, item_id))
                    cursor.close()

                if size:
                    # Update size in cart_items table
                    cursor = get_cursor()
                    cursor.execute("UPDATE cart_items SET size = %s WHERE id = %s", (size, item_id))
                    cursor.close()

    # Fetch all cart items from the database after the update
    cursor = get_cursor()
    cursor.execute("SELECT cart_items.id, cart_items.product_id, cart_items.size, cart_items.quantity, "
                   "products.product_name, products.price, products.image_name "
                   "FROM cart_items JOIN products ON cart_items.product_id = products.id")
    cart_items = cursor.fetchall()
    cursor.close()

    return jsonify({'cart_items': cart_items})

@app.route('/view_cart')
def view_cart_route():
    # Fetch all orders using the view_cart function
    orders = view_cart()

    # Calculate the total amount
    total_amount = sum(order['price'] * order['quantity'] for order in orders)

    # Check if the client accepts HTML
    if 'text/html' in request.accept_mimetypes:
        return render_template('orderlist.html', orders=orders, total_amount=total_amount)
    else:
        # Return a JSON response
        return jsonify({'orders': orders, 'total_amount': total_amount})

if __name__ == '__main__':
    app.run(debug=True)