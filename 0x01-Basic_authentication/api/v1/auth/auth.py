#!/usr/bin/python3
"""
The authentication class is defined Here
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    defines clients right and entitlement to specific server resources
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path.
        Args:
        path (str): The path to check.
            excluded_paths (List[str]): List of excluded paths.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True

        slash_handler = [path, path + "/"]

        if not excluded_paths:
            return True

        for excluded in excluded_paths:
            if excluded.endswith('/') and excluded.startswith(path):
                return False
            if excluded in slash_handler:
                return False

        return True

    def authorization_header(self, request: request = None) -> str:
        """
        handles header used by the client when making request
        """
        return None

    def current_user(self, request: request = None) -> TypeVar('User'):
        """
        idenrifies with the current user
        """
        return None
