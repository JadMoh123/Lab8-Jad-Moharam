#!/usr/bin/python
import os
import sqlite3
from flask import Flask, jsonify

DB_PATH = 'database.db'

# users added to the database the first time the app runs
INITIAL_USERS = [
    ("John Doe", "jondoe@gamil.com", "067765434567", "John Doe Street, Innsbruck", "Austria"),
    ("Jane Smith", "janesmith@gmail.com", "071234567", "Bliss Street, Beirut", "Lebanon"),
    ("Ali Hassan", "alihassan@gmail.com", "03111222", "Hamra Street, Beirut", "Lebanon"),
]


def connect_to_db():
    return sqlite3.connect(DB_PATH)


def init_db():
    first_run = not os.path.exists(DB_PATH)
    conn = connect_to_db()
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            );
        ''')
        if first_run:
            conn.executemany(
                "INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)",
                INITIAL_USERS)
        conn.commit()
    finally:
        conn.close()


def get_user_names():
    conn = connect_to_db()
    try:
        rows = conn.execute("SELECT name FROM users ORDER BY user_id").fetchall()
        return [row[0] for row in rows]
    finally:
        conn.close()


app = Flask(__name__)


@app.route('/get_users', methods=['GET'])
def get_users():
    """Return the names of all the users in the database."""
    return jsonify(get_user_names())


if __name__ == "__main__":
    init_db()
    # 0.0.0.0 so the API is reachable from outside the container
    app.run(host="0.0.0.0", port=3000)
