#!/usr/bin/env python3
"""
simple flask application
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def welcome_message() -> str:
    """
    return json message, precisely a welcome message
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
        user = AUTH.register_user(email, password)
        return jsonify(
                {
                    "email": user.email,
                    "message": "user created"
                    }
                )
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """"
    creates a swssion id for the user, if the user login
    parameters are accurate
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> None:
    """
    a route to delete a session id pet user request
    logs a user out of a session
    """
    session_id = request.cookies.get("session_id")

    try:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            # note return redirect(url_for("welcome_message")) also works
            return redirect("/")
        else:
            abort(403)
    except NoResultFound:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def user_profile():
    """
    get the user or user using a session id
    """
    session_id = request.cookies.get("session_id")
    try:
        user = AUTH.get_user_from_session_id(session_id)
        if user is None:
            abort(403)
        return jsonify({"email": user.email}), 200
    except NoResultFound:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    reses/update a users password token
    """
    email = request.form.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify(
                {
                    "email": email,
                    "reset_token": reset_token
                    }
                ), 200

    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    This route will update the users passeord, to his new chosen password
    provided he has a valid token
    """
    email = request.form.get("email")
    new_password = request.form.get("new_password")
    reset_token = request.form.get("reset_token")

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200

    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
