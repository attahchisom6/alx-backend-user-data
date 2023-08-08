#!/usr/bin/env python3
"""
A child class of the auth class
"""
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
        method that returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if base64_authorization_header is None:
            return None

        if type(base64_authorization_header) is not str:
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
        except Exception:
            return None

        return decoded_bytes.decode("utf-8")

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """
        method that returns the user email and password
        from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if type(decoded_base64_authorization_header) is not str:
            return (None, None)

        if ":" not in decoded_base64_authorization_header:
            return (None, None)

        listt = decoded_base64_authorization_header.split(":")
        return (listt[0], listt[1])
