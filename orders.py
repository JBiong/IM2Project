from database import fetchone, fetchall

def create_order(product_name, size, quantity):
    order_data = {
        "product_name": product_name,
        "size": size,
        "quantity": quantity
    }

    query = "CALL create_order(%s, %s, %s, %s)"
    params = (
        order_data["product_name"],
        order_data["size"],
        order_data["quantity"]
    )

    result = fetchone(query, params)

    # Assuming your stored procedure or database operation returns an ID for the created order
    return result["id"]

def get_orders():
    query = "SELECT * FROM get_orders"  # Adjust the query based on your database structure
    result = fetchall(query)
    return result

def get_order(order_id):
    query = "SELECT * FROM get_orders WHERE id = %s"  # Adjust the query based on your database structure
    params = (order_id,)
    result = fetchone(query, params)
    return result

def update_order(order_id, size, quantity):
    query = "CALL update_order(%s, %s, %s)"
    params = (order_id, size, quantity)
    result = fetchone(query, params)
    return result["id"]

def delete_order(order_id):
    query = "CALL delete_order(%s)"
    params = (order_id,)
    result = fetchone(query, params)
    return result["id"]
