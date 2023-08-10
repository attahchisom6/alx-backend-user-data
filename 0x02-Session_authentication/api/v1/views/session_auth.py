#!/usr/bin/env python3
"""
A view for all session authenication routes
"""
from flask import request, jsonify
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth
import os


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def handle_user_login():
    """
    method to handles user login using session authentication
    """
    email = request.form.get("email")
    password = request.form.get("password")

    email_error = {"error": "email missing"}
    pwd_error = {"error": "password missing"}

    if email is None or email == "":
        return jsonify(email_error), 400

    if password is None or password == "":
        return jsonify(pwd_error), 400

    user = User()
    user_list = user.search({"email": email})
    if not user_list:
        return jsonify({"error": "no user found for this email"}), 404

    from api.v1.app import auth
    users_with_password = []
    for users in user_list:
        if not users.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        else:
            users_with_password.append(users)
    user = users_with_password[0]

    session_id = auth.create_session(user.id)

    response = jsonify(user.to_json())

    session_name = os.getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)

    return response


@app_views.route("/auth_session/logout", methods=["DELETE"],
                 strict_slashes=False)
def logout_route():
    """
    a route to log a user out of the current session
    """
    if request is not None:
        is_deleted = auth.delete_session(request)
        if is_deleted is False:
            abort(404)
        return jsonify({}), 200
    abort(404)
