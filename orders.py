from database import fetchone, fetchall
from flask import current_app
from flask_mysqldb import MySQL

from database import fetchone, fetchall

# Modify these functions to use stored procedures and views
def add_to_cart(product_id, size, quantity):
    query = "CALL add_to_cart(%s, %s, %s)"
    params = (product_id, size, quantity)
    result = fetchone(query, params)
    return result

def edit_cart(item_id, new_quantity, new_size):
    query = "CALL edit_cart(%s, %s, %s)"
    params = (item_id, new_quantity, new_size)
    result = fetchone(query, params)
    return result

def view_cart():
    query = "SELECT * FROM view_cart"
    result = fetchall(query)
    return result

def update_cart_item(item_id, new_quantity, new_size):
    # mysql = current_app.config['mysql']
    query = "CALL update_cart_item(%s, %s, %s)"
    params = (item_id, new_quantity, new_size)
    result = fetchone(query, params)
    return result

def delete_cart_item(item_id):
    # mysql = current_app.config['mysql']
    query = "CALL delete_cart_item(%s)"
    params = (item_id,)
    result = fetchone(query, params)
    return result

def create_order(product_name, size, quantity):
    order_data = {
        "product_name": product_name,
        "size": size,
        "quantity": quantity
    }

    mysql = current_app.config['mysql']

    cursor = mysql.connection.cursor()
    cursor.callproc("create_order", [order_data["product_name"], order_data["size"], order_data["quantity"]])
    mysql.connection.commit()

    # Assuming your stored procedure or database operation returns an ID for the created order
    cursor.execute("SELECT LAST_INSERT_ID() AS id")
    result = cursor.fetchone()
    cursor.close()

    return result["id"]

def get_orders():
    mysql = current_app.config['mysql']

    cursor = mysql.connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM get_orders")  # Adjust the query based on your database structure
    result = cursor.fetchall()
    cursor.close()

    return result

def get_order(order_id):
    mysql = current_app.config['mysql']

    cursor = mysql.connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM get_orders WHERE id = %s", (order_id,))  # Adjust the query based on your database structure
    result = cursor.fetchone()
    cursor.close()

    return result

def update_order(order_id, size, quantity):
    mysql = current_app.config['mysql']

    cursor = mysql.connection.cursor()
    cursor.callproc("update_order", [order_id, size, quantity])
    mysql.connection.commit()

    # Assuming your stored procedure or database operation returns an ID for the updated order
    cursor.execute("SELECT %s AS id", (order_id,))
    result = cursor.fetchone()
    cursor.close()

    return result["id"]

def delete_order(order_id):
    mysql = current_app.config['mysql']

    cursor = mysql.connection.cursor()
    cursor.callproc("delete_order", [order_id])
    mysql.connection.commit()

    # Assuming your stored procedure or database operation returns an ID for the deleted order
    cursor.execute("SELECT %s AS id", (order_id,))
    result = cursor.fetchone()
    cursor.close()

    return result["id"]
