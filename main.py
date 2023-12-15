import os
from flask import Flask,jsonify,request,render_template,flash,redirect,url_for
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from users import create_user,authenticate_user,get_users,get_user
from orders import get_all_products,create_order
from database import set_mysql
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)



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

app.secret_key = os.getenv("FLASK_SECRET_KEY", "your_secret_key_here")

app.template_folder = "template"
app.static_folder = "static"


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
        user = get_user(id)
        return jsonify(user)
    

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route('/products')
def get_products():
    products = get_all_products()

    product_list = [
        {
            'id': product['id'],
            'category': product['category'],
            'name': product['product_name'],
            'stock': product['product_stock'],
            'price': float(product['price']),
            'image_name': product['image_name']
        }
        for product in products
    ]

    if request.headers.get('Content-Type') == 'application/json':
        return jsonify(products=product_list)
    else:
        return render_template("index.html", products=product_list)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        size = data.get('size')

      
        if product_id is not None and quantity is not None and size is not None:
            # Call your create_order function here
            order_id = create_order(product_id, quantity, size)
            print("ID:",order_id)
            return jsonify({'status': 'success', "order_id": order_id})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid data format'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500