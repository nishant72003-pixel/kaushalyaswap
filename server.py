from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # enable CORS so frontend (GitHub Pages) can talk to backend

# simple health check
@app.route("/")
def home():
    return "Backend is running!"

# signup API
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = users_collection.find_one({"email": email, "password": password})
    if user:
        return jsonify({
            "message": "Login successful!",
            "user": {
                "name": user.get("name"),
                "skill": user.get("skill")
            }
        }), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401
