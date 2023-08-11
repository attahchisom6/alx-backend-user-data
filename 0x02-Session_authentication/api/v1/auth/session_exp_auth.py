#!/usr/bin/env python3
"""
This module will handle session expirement
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
    sclass to handle expires auth sessions
    """
    def __init__(self):
        """
        overloads the constructor for the main class
        """
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION"))
        except (ValueError, TypeError):
            self.session_duration = 0
        self.session_dictionary = None

    def create_session(self, user_id=None):
        """
        creqte a session id for a given user id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.session_dictionary = {
                "user_id": user_id,
                "created_at": datetime.now()
                }

        self.user_id_by_session_id[session_id] = self.session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        return the user for the given session, it overload the original
        method from the parent class
        """
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id.keys():
            return None

        self.session_dictionary = self.user_id_by_session_id.get(session_id)
        if self.session_dictionary is None:
            return None

        if "created_at" not in self.session_dictionary.keys():
            return None

        created_at = self.session_dictionary["created_at"]

        # check if session has expired
        current_time = datetime.now()
        session_time = created_at + timedelta(seconds=self.session_duration)

        if self.session_duration > 0 and session_time < current_time:
            return None

        user_id = self.session_dictionary.get("user_id")
        if user_id is None:
            return None

        if self.session_duration <= 0:
            return user_id

        return user_id
