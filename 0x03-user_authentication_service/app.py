#!/usr/bin/env python3
"""
Basic Flask app
"""

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/users', methods=['POST'])
def register_user():
    """Register a new user route"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        # registering a user
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        # If the user already exists, return a 400 error
        return jsonify({"message": "email already registered"}), 400


@app.route("/")
def index():
    """GET route that returns welcominh message
        in json format"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
