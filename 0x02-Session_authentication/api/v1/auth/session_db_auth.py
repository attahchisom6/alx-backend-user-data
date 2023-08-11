#!/usr/bin/env python3
"""
module for session storage
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    store user data and session to a file storage
    """
    def create_session(self, user_id=None):
        """
        overloads the original method from the parent, return its own session
        """
        if user_id is None:
            return None

        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        session_dictionary = {
                "user_id": user_id,
                "session_id": session_id
            }

        user_session = UserSession(**session_dictionary)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        retrieve user id from its session_id for storage
        """
        if session_id is None:
            return None

        UserSession.load_from_file()
        user_sessions = UserSession.search({"session_id": session_id})

        if not user_sessions:
            return None

        # we use the first item in the list becos we believe that the list
        # returned only one unique session_id that we wantd
        created_at = user_sessions[0].created_at

        current_time = datetime.utcnow()
        session_time = created_at + timedelta(seconds=self.session_duration)

        if session_time < current_time:
            return None

        return user_sessions[0].user_id

    def destroy_session(self, request=None):
        """
        destroy a user bases on the session id
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(user_id)
        if user_id is None:
            False

        user_sessions = UserSession.search({"session_id": session_id})

        if user_sessions is None:
            return False

        try:
            user_sessions[0].remove()
            UserSession.save_to_file()
        except Exception:
            return False
        return True
