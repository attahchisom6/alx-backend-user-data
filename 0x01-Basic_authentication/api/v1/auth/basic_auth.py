#!/usr/bin/env python3
"""
A child class of the auth class
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


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

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
        that returns the User instance based on his email and password
        """
        if user_email is None or type(user_email) is not str:
            return None

        if user_pwd is None or type(user_pwd) is not str:
            return None

        user = User()
        users_list = user.search({"email": user_email})
        if users_list is None:
            return None

        user_with_valid_pwd = []
        try:
            for user in users_list:
                if user.is_valid_password(user_pwd):
                    user_with_valid_pwd.append(user)

            return user_with_valid_pwd[0]
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        that overloads Auth and retrieves the User instance
        for a request:
        """
        user = None
        auth_header = self.authorization_header(request)

        bs64_header = self.extract_base64_authorization_header(auth_header)

        decoded_header = self.decode_base64_authorization_header(bs64_header)

        user_email, user_pwd = self.extract_user_credentials(decoded_header)

        user = self.user_object_from_credentials(user_email, user_pwd)

        return user
