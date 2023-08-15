#!/usr/bin/env python3
"""
This module defines everything we use for authentication
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    method that converts a stringed password to a hashed bytes
    password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str):
        """
        register a user and save to the database
        """
        db = self._db._session
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("{} already exists".format(email))

        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = User(email=email, hashed_password=hashed_password)

            db.add(new_user)
            db.commit()
            return new_user
