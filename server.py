from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables (for MongoDB)
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Connect MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["kaushalyaswap"]
users = db["users"]

@app.route("/")
def home():
    return render_template("get-started.html")

@app.route("/signup", methods=["POST"])
def signup():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    skill = request.form.get("skill")

    # Check if user already exists
    if users.find_one({"email": email}):
        return "⚠️ User already exists. Please Sign In."

    # Insert new user
    users.insert_one({
        "name": name,
        "email": email,
        "password": password,
        "skill": skill
    })

    # Save session and go to dashboard
    session["user"] = {"name": name, "email": email, "skill": skill}
    return redirect(url_for("dashboard"))

@app.route("/signin", methods=["POST"])
def signin():
    email = request.form.get("email")
    password = request.form.get("password")

    user = users.find_one({"email": email, "password": password})
    if user:
        session["user"] = {"name": user["name"], "email": user["email"], "skill": user["skill"]}
        return redirect(url_for("dashboard"))
    else:
        return "❌ Invalid email or password."

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", name=session["user"]["name"], skill=session["user"]["skill"])
    return redirect(url_for("home"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
