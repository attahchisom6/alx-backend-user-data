#!/usr/bin/env python3
"""
The authentication class is defined Here
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    defines clients right and entitlement to specific server resources
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path.
        in this method we will define which routes doesn't need authentication
        Args:
        path (str): The path to check.
            excluded_paths (List[str]): List of excluded paths.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True

        handle_slashed_path = [path, path + "/"]

        # all path in excluded path doesn't need authentication
        if not excluded_paths:
            return True

        for excluded in excluded_paths:
            if excluded.endswith('*') and path.startswith(excluded[:-1]):
                return False
            if excluded in handle_slashed_path:
                return False

        return True

    def authorization_header(self, request: request = None) -> str:
        """
        handles header used by the client when making request
        """
        if request is None:
            return None

        key = "Authorization"
        dictt_headers = request.headers
        if key not in dictt_headers:
            return None
        return dictt_headers.get(key)

    def current_user(self, request: request = None) -> TypeVar('User'):
        """
        idenrifies with the current user
        """
        return None

    def session_cookie(self, request=None):
        """
        method that returns cookie value from a request,
        Note: This value is often andi in our case a session id
        """
        if request is None:
            return None

        cookie = request.cookies
        if cookie is None:
            return None

        session_name = os.getenv("SESSION_NAME")
        if session_name is None:
            return None

        return cookie.get(session_name)
