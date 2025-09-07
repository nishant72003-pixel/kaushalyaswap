from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔹 Update with your MongoDB Atlas connection string
app.config["MONGO_URI"] = "your_mongodb_connection_uri"

mongo = PyMongo(app)
users = mongo.db.users


# ---------------- SIGNUP ----------------
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    skill = data.get("skill")

    if not name or not email or not password or not skill:
        return jsonify({"message": "All fields are required"}), 400

    if users.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    users.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password,
        "skill": skill
    })

    return jsonify({
        "message": "Signup successful!",
        "user": {"name": name, "skill": skill}
    }), 201


# ---------------- LOGIN ----------------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    user = users.find_one({"email": email})
    if user and check_password_hash(user["password"], password):
        return jsonify({
            "message": "Login successful!",
            "user": {"name": user["name"], "skill": user["skill"]}
        }), 200

    return jsonify({"message": "Invalid email or password"}), 401


# ---------------- ROOT ----------------
@app.route("/")
def home():
    return "Backend is running with MongoDB!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
