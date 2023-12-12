from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, template_folder=os.path.abspath('templates'))

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/shoppingapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(45), nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    category = db.Column(db.String(45), nullable=False)
    image_name = db.Column(db.String(45), nullable=False)

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    size = db.Column(db.String(45), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Define the relationship with the Product model
    product = db.relationship('Product', backref='cart_items')

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    size = db.Column(db.String(45), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Define the relationship with the Product model
    product = db.relationship('Product', backref='orders')

# Create the tables within the application context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Fetch all products from the database (for dropdown)
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()

    # Assuming the data follows the expected format
    category = data.get('category')
    name = data.get('name')
    price = data.get('price')
    image_name = data.get('image_name')

    # Create a new product
    new_product = Product(category=category, product_name=name, price=price, image_name=image_name)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product created successfully", "product_id": new_product.id})

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    total_products = 30  # Assuming you have 2 dresses

    for dress_number in range(1, total_products + 1):
        product_id = request.form.get(f'product_id{dress_number}')
        size = request.form.get(f'size{dress_number}', '')  # Default to an empty string if not specified

        # Check if the product is selected
        if not product_id:
            continue

        try:
            product_id = int(product_id)
        except ValueError:
            # Handle invalid input
            return redirect(url_for('index'))

        # Check if the quantity is provided, default to 0 if not
        quantity = request.form.get(f'quantity{dress_number}', 0)

        try:
            quantity = int(quantity)
        except ValueError:
            # Handle invalid input
            return redirect(url_for('index'))

        # Check if the quantity is greater than 0 before adding to the cart
        if quantity > 0:
            # Check if the product is already in the cart
            existing_cart_item = CartItem.query.filter_by(product_id=product_id, size=size).first()

            if existing_cart_item:
                # Update the quantity if the item already exists in the cart
                existing_cart_item.quantity += quantity
            else:
                # Create a new cart item if the item is not in the cart
                cart_item = CartItem(product_id=product_id, size=size, quantity=quantity)
                db.session.add(cart_item)

            # Create a new order
            order = Order(product_id=product_id, size=size, quantity=quantity)
            db.session.add(order)

    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
