#!/usr/bin/env python3
"""
This module defines everything we use for authentication
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    method that converts a stringed password to a hashed bytes
    password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:

    """
    generate a string uuid identify private to this module and
    shoudn't  be used outside it
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register a user and save to the database
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))

        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        checks if the user instance loggin in is a valid user
        Args:
            email: user email
            password: password
        Return:
            True if email and password are valid
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode("utf-8"),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        a method that creates a user session id based on his emial
        """
        try:
            session_id = _generate_uuid()
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)

            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[None, User]:
        """
        get a user corresponding to a given session id
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)

            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        destroys a session by the session_id of a given user id to None
        """
        return self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        creates a random uuid that will seeve as a reset token for a given user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def reset_password(self, reset_token: str, password: str) -> None:
        """
        takes reset token and resets the password of the user
        """
        if password is None or reset_token is None:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        """kwargs = {
                "hashed_password": hashed_password,
                "reset_token": None
            }"""

        self._db.update_user(user.id,
                             hashed_password=hashed_password,
                             reset_token=reset_token)
