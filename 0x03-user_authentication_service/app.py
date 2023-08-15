#!/usr/bin/env python3
"""
simple flask application
"""
from flask import Flask, jsonify
from auth import Auth
from user import User
from sqlalchemy.exc import NoResultFound


app = Flask(__name__)
Auth = Auth()


@app.route("/", method=["GET"], strict_slashes=False)
def json_message():
    """
    return json message
    """
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"], strict_slashes=False)
def users(email:str, password: str) -> User:
    """
    a route/endpoint to register users
    """
    try:
        user = Auth.register_user(email, password)
        return jsonify({"message": "email already exists"}), 400

    except NoResultFound:
        return jsonify(
                {
                    "email": email,
                    "message": "user created"
                    }
                )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=500)
