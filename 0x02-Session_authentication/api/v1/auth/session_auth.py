#!/usr/bin/env python3
""""
This module defines another authentication mechanism
called a session authentications
"""
from api.v1.auth.auth import Auth
from models.user import User
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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        method that returns a user id based on session id
        """
        if session_id is None:
            return None

        if type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        method that overloads the 'current_user' method in the
        parent class, returning a user id based on the cookie
        _my_session_id
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        user = User()
        user = user.get(user_id)

        if not user:
            return None
        return user

    def destroy_session(self, request=None):
        """
        method that delete a user session
        """
        if request is None:
            return False

        if not self.session_cookie(request):
            return False
        sesssion_id = self.session_cookie(request)

        if not self.user_id_for_session_id(session_id):
            return False

        del self.user_id_by_session_id[session_id]
        return True
