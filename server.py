from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["kaushalyaswap"]
users = db["users"]

# ✅ Route: Signup
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    skill = data.get("skill")

    if users.find_one({"email": email}):
        return jsonify({"message": "Email already exists!"}), 400

    users.insert_one({
        "name": name,
        "email": email,
        "password": password,   # ⚠️ (for now plain text, later we’ll hash)
        "skill": skill
    })

    return jsonify({"message": "Signup successful!"}), 201

# ✅ Route: Signin
@app.route("/signin", methods=["POST"])
def signin():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = users.find_one({"email": email, "password": password})
    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify({
        "message": "Signin successful!",
        "name": user["name"],
        "skill": user["skill"]
    }), 200


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend is running!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
