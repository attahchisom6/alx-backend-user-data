#!/usr/bin/env python3
"""
simple flask application
"""
from flask import Flask, jsonify, request
from auth import Auth
from user import User


app = Flask(__name__)
Auth = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def json_message():
    """
    return json message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """
    a route/endpoint to register users
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = Auth.register_user(email, password)
        return jsonify(
                {
                    "email": user.email,
                    "message": "user created"
                    }
                )
    except ValueError:
        return jsonify({"message": "email already registered"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
