import os
import re
import sqlite3
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from flask_cors import CORS

DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

NUMERIC_PW_REGEX = re.compile(r"^[0-9]{1,8}$")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                teach TEXT NOT NULL,
                learn TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")

init_db()

@app.get('/api/health')
def health():
    return jsonify({"ok": True})

@app.post('/api/signup')
def signup():
    data = request.get_json(silent=True) or {}
    required = ['name', 'email', 'password', 'teach', 'learn']
    missing = [k for k in required if not data.get(k)]
    if missing:
        return jsonify({"ok": False, "error": f"Missing fields: {', '.join(missing)}"}), 400

    password = str(data['password'])
    if not NUMERIC_PW_REGEX.match(password):
        return jsonify({"ok": False, "error": "Password must be only numbers and up to 8 digits."}), 400

    pw_hash = generate_password_hash(password)

    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO users(name, email, password_hash, teach, learn) VALUES(?,?,?,?,?)",
                (data['name'].strip(), data['email'].strip().lower(), pw_hash, data['teach'].strip(), data['learn'].strip()),
            )
    except sqlite3.IntegrityError:
        return jsonify({"ok": False, "error": "Email already registered."}), 409

    return jsonify({"ok": True, "message": "Signup saved."}), 201

@app.get('/api/users')
def list_users():
    with get_conn() as conn:
        rows = conn.execute("SELECT id, name, email, teach, learn, created_at FROM users ORDER BY id DESC").fetchall()
        users = [dict(r) for r in rows]
    return jsonify({"ok": True, "users": users})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
