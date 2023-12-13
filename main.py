import os
from flask import Flask,jsonify,request,render_template,flash,redirect,url_for
from flask_mysqldb import MySQL
from users import create_user,authenticate_user,get_users
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
        user = get_users(id)
        return jsonify(user)
    

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")





