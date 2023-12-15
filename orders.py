from database import fetchone, fetchall

def get_all_products():
    query = "SELECT * FROM products"  
    result = fetchall(query)
    return result

def create_order(product_id, quantity, size):
    product = get_product_by_id(product_id)

    if product:
        query = "CALL create_order(%s, %s, %s)" 
        params = (product_id, quantity, size)
        result = fetchone(query, params)
        order_id = result["order_id"] if result else None
        return order_id

def get_product_by_id(product_id):
    query = "SELECT * FROM products WHERE id = %s"  
    params = (product_id,)
    result = fetchone(query, params)
    return result








# def get_orders():
#     query = "SELECT * FROM get_orders"  
#     result = fetchall(query)
#     return result

# def get_order(order_id):
#     query = "SELECT * FROM get_orders WHERE id = %s"  
#     params = (order_id,)
#     result = fetchone(query, params)
#     return result

# def update_order(order_id, size, quantity):
#     query = "CALL update_order(%s, %s, %s)"
#     params = (order_id, size, quantity)
#     result = fetchone(query, params)
#     return result["id"]

# def delete_order(order_id):
#     query = "CALL delete_order(%s)"
#     params = (order_id,)
#     result = fetchone(query, params)
#     return result["id"]