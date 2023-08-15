#!/usr/bin/env python3
"""
This module defines everything we use for authentication
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


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
    return str(uuid.uuid4())


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
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password
                )
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """"
        creates a session id based on a given user emial and stores
        it in the database
        """
        db = self._db._session

        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            db.commit()

            return session_id
        except NoResultFound:
            return None
