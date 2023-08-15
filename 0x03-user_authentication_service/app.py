#!/usr/bin/env python3
"""
simple flask application
"""
from flask import Flask, jsonify, request, abort
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


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """"
    creates a swssion id for the user, if the user login
    parameters are accurate
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        if Auth.valid_login(email, password):
            session_id = Auth.create_session(email)
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response
        else:
            abort(401)
    except ValueError:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
