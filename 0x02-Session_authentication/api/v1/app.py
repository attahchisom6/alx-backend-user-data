#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth


auth = None
basic_auth = None
session_auth = None


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


auth_type = os.getenv("AUTH_TYPE")
if auth_type:
    if auth_type == "auth":
        auth = Auth()
    elif auth_type == "basic_auth":
        auth = BasicAuth()
    elif auth_type == "session_auth":
        auth = SessionAuth()


@app.before_request
def handle_before_request():
    """
    handles fistly certain action before a request is processed
    """
    if auth is None:
        return

    api_list = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/'
        ]
    if not auth.require_auth(request.path, api_list):
        return

    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)
    request.current_user = auth.current_user(request)

def session_cookie(self, request=None):
    """
    method that returns cookie value from a request
    """
    if request is None:
        return None

    session_name = os.getenv("SESSION_NAME")
    cookie = request.cookie
    cookie["_my_session_id"] = session_name

    return cookie.get("_my_session_id")


@app.errorhandler(404)
def not_found(error):
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorised_error(error) -> str:
    """
    handles unauthorized acess to the api
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error) -> str:
    """
    returns a forbidden message, when trying to access perhaps the creator
    or server retricted items. e.g limited editions
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
