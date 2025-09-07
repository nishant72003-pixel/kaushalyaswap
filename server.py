from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # enable CORS so frontend (GitHub Pages) can talk to backend

# simple health check
@app.route("/")
def home():
    return "Backend is running!"

# signup API
@app.route("/api/signup", methods=["POST"])
def signup():
    try:
        data = request.json  # get JSON body
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        teach = data.get("teach")
        learn = data.get("learn")

        # ✅ in real projects you’d save this to MongoDB or SQL
        print(f"New signup: {name}, {email}, teach={teach}, learn={learn}")

        return jsonify({"message": "Signup successful!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
