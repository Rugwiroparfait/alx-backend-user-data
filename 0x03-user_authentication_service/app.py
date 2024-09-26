#!/usr/bin/env python3
"""
Basic Flask app to register users, log them in, and provide a welcome message.
This app uses the Auth class to manage user registration and session management.
"""

from flask import Flask, jsonify, request, abort, make_response
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
        return jsonify({"message": "email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> jsonify:
    """
    POST route to log in a user.
    
    Expects 'email' and 'password' in the request form data.
    If credentials are valid, creates a session ID and sets it in a cookie.
    If invalid, returns a 401 error.
    
    Returns:
        JSON response with a success or error message.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)

    if not AUTH.valid_login(email, password):
        abort(401)

    # Create session ID
    session_id = AUTH.create_session(email)

    if not session_id:
        abort(401)

    # Create response and set session_id in a cookie
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


@app.route("/", methods=['GET'])
def index() -> jsonify:
    """
    GET route that returns a welcome message in JSON format.
    
    Returns:
        JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    # Running the Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)

