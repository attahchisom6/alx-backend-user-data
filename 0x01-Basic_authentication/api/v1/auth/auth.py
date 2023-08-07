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
        defines authentication requirements
        """
        return False

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
