#!/usr/bin/env python3
"""
Basic Flask app to register users and provide a welcome message.
This app uses the Auth class to manage user registration.
"""

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/users', methods=['POST'])
def register_user() -> jsonify:
    """
    POST route to register a new user.
    
    Expects 'email' and 'password' in the request form data.
    If successful, returns the email and a success message.
    If the email is already registered, returns an error message.
    
    Returns:
        JSON response with a success or error message.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        # Handle missing email or password
        return jsonify({"message": "email and password are required"}), 400

    try:
        # Registering a user via the Auth class
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        # If the user already exists, return a 400 error
        return jsonify({"message": "email already registered"}), 400


@app.route("/", methods=['GET'])
def index() -> jsonify:
    """
    GET route that returns a welcome message in JSON format.
    
    Returns:
        JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    # Running the Flask app in debug mode
    app.run(host="0.0.0.0", port=5000, debug=True)

