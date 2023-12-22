from database import fetchone,fetchall

def create_user(name, age, email, password, is_login=False):
    username = email
    query = "CALL create_user(%s, %s, %s, %s, %s)"
    params = (name, age, email, username, password)
    result = fetchone(query, params)

    if is_login:
        return result
    else:
        return result["id"]

def get_users():
  query = "SELECT * FROM get_users"
  result = fetchall(query)
  return result


def authenticate_user(username, password):
    user = get_user_by_email(username)

    if user and user["password"] == password:
        return user
    else:
        return None

def get_user_by_email(username):
    query = "SELECT * FROM users WHERE username = %s"
    params = (username,)
    result = fetchone(query, params)
    return result

def get_users(id):
    query = "SELECT * FROM get_users WHERE id = %s"
    params = (id,)
    result = fetchone(query, params)
    return result