#!/usr/bin/env python3

from flask import Flask, request, jsonify, render_template
import sqlite3
import hashlib

app = Flask(__name__, static_folder='static', static_url_path="/")

def check_no_more_leaks(username: str,password: str) -> bool :
    # Create SHA256 hash of the concatenated username and password
    sha256_hash = hashlib.sha256(f'{username}{password}'.encode()).hexdigest()

    conn = sqlite3.connect('../data/nomoreleaks.sqlite3')
    c = conn.cursor()
    c.execute('SELECT hash FROM hashes WHERE hash = ?', (sha256_hash,))
    result = c.fetchone()
    conn.close()
    if result:
        return True
    return False

@app.route('/login', methods=['POST'])

def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    result = {}
    result["NoMoreLeaks"] = check_no_more_leaks(username, password)

    return jsonify(result), 200

#@app.route('/')
#def index():
#    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)