#!/usr/bin/env python3
"""
This module defines everything we use for authentication
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


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
            user.session_id = session_id

            self._db._session.commit()

            return session_id
        except NoResultFound:
            return None
