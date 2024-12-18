# AmlShop

AmlShop is a comprehensive clothing store web application. It provides a seamless shopping experience with features like product browsing,
shopping cart management, order handling, and user authentication. Developed with Flask (Python) and powered by MySQL, the system ensures 
efficient data management and scalability.


# Features

User Authentication:

  - Users can sign up and log in to access their personalized shopping experience.

Product Browsing:

- View available products with details like name, size, and price.

Shopping Cart Management:

- Add products to the cart with specific sizes and quantities.

- Edit cart items by updating sizes and quantities.

- View all items in the cart.

- Delete items from the cart.

Order Management:

- Create new orders from the shopping cart.

- View all orders or specific orders.

- Update order details like size and quantity.

- Delete orders as needed.

Stored Procedures and Views:

- Optimized database operations for better performance and maintainability.

# Technology Stack

- Backend: Flask (Python)
- Database: MySQL
- Frontend: (Integrate as needed)
- Database Operations: Utilizes stored procedures and views for efficient CRUD operations.

# Installation and Setup
- **Clone the Repository**:
  - Run the following commands to clone and navigate to the project directory:
    ```bash
    git clone https://github.com/your-repo/amlshop.git
    cd amlshop
    ```
- **Install Dependencies**:
  - Ensure Python and pip are installed, then execute:
    ```bash
    pip install -r requirements.txt
    ```
- **Configure MySQL**:
  - Set up a MySQL database:
    - Import the required schema and stored procedures (e.g., `schema.sql`).
    - Update the database configuration in the Flask application:
      ```python
      app.config['MYSQL_HOST'] = 'your-host'
      app.config['MYSQL_USER'] = 'your-user'
      app.config['MYSQL_PASSWORD'] = 'your-password'
      app.config['MYSQL_DB'] = 'your-database'
      ```
- **Run the Application**:
  - Start the Flask development server with:
    ```bash
    flask run
    ```
- **Access the Application**:
  - Open a web browser and navigate to `http://127.0.0.1:5000`.
 
# API Endpoints

User Authentication

- Sign Up: POST /signup

- Log In: POST /login

Product Management

- View Products: GET /products

Shopping Cart Management

- Add to Cart: POST /cart

- View Cart: GET /cart

- Edit Cart Item: PUT /cart/<item_id>

- Delete Cart Item: DELETE /cart/<item_id>

Order Management

- Create Order: POST /orders

- View Orders: GET /orders

- View Specific Order: GET /orders/<order_id>

- Update Order: PUT /orders/<order_id>

- Delete Order: DELETE /orders/<order_id>

Database Schema and Procedures

Stored Procedures

- add_to_cart: Adds a product to the cart.

- edit_cart: Edits the quantity and size of a cart item.

- update_cart_item: Updates cart items.

- delete_cart_item: Removes an item from the cart.

- create_order: Creates a new order.

- update_order: Updates the size and quantity of an order.

- delete_order: Deletes an order.

Views

- view_cart: Displays all items in the user's cart.

- get_orders: Displays all orders for the user.

Developed with ❤️ using Flask and MySQL.



