from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
db_path = "chat.db"

# Inisialisasi database
def init_db():
    with sqlite3.connect(db_path) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            message TEXT
        )''')

init_db()

@app.route("/")
def home():
    return "✅ Server Flask Taufiq aktif & online!"

@app.route("/send", methods=["POST"])
def send_message():
    data = request.get_json()
    username = data.get("username")
    message = data.get("message")
    with sqlite3.connect(db_path) as conn:
        conn.execute("INSERT INTO chat (username, message) VALUES (?, ?)", (username, message))
        conn.commit()
    return jsonify({"status": "sent", "username": username, "message": message})

@app.route("/messages", methods=["GET"])
def get_messages():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("SELECT username, message FROM chat ORDER BY id DESC LIMIT 20")
        messages = [{"username": u, "message": m} for u, m in cursor.fetchall()]
    return jsonify(messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
