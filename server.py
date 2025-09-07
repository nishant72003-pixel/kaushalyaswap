from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecret"  # needed for session

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["kaushalyaswap"]
users_collection = db["users"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.form
    user = {
        "name": data["name"],
        "email": data["email"],
        "password": data["password"],
        "skill": data["skill"]
    }

    # Check if user exists
    if users_collection.find_one({"email": user["email"]}):
        return "User already exists, please sign in!"

    # Insert new user
    users_collection.insert_one(user)
    session["user"] = user
    return redirect(url_for("dashboard"))

@app.route("/signin", methods=["POST"])
def signin():
    data = request.form
    user = users_collection.find_one({"email": data["email"], "password": data["password"]})

    if user:
        session["user"] = user
        return redirect(url_for("dashboard"))
    else:
        return "Invalid email or password"

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        user = session["user"]
        return render_template("dashboard.html", user=user)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
