#!/usr/bin/env python3
"""
A child class of the auth class
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    a child authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        method  that returns the Base64 part of the Authorization header
        for a Basic Authentication.
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None

            value = authorization_header[6:]
            return value
