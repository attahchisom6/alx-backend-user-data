#!/usrlbin/env python3
"""
Module made to store user sessions so that no ids are lost after each
session
"""
from models.base import Base


class UserSession(Base):
    """
    User class to handle session storage
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
        initalizing instances for user_id and session id
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
