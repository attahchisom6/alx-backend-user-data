#!/usr/bin/env python3
""""
This module defines another authentication mechanism
called a session authentication
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    A session authentication class that inherits from
    the Auth authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        method that creates a session id for a given user_id
        """
        if user_id is None:
            return None

        if type(user_id) is not str:
            return None

        session_id = str(uuid.uuid4())
        key = session_id
        self.user_id_by_session_id[key] = user_id
        return key
