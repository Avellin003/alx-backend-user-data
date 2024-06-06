#!/usr/bin/env python3
"""
SessionExpAuth class definition
"""
import os
from datetime import (
    datetime,
    timedelta
)

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class that includes an expiration date to a Session ID
    """
    def __init__(self):
        """
        Class initialization
        """
        try:
            duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """
        Generates a Session ID for a user_id
        """
        sessionid = super().create_session(user_id)
        if sessionid is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[sessionid] = session_dictionary
        return sessionid

    def user_id_for_session_id(self, session_id=None):
        """
        Gets a user ID from a session ID
        """
        if session_id is None:
            return None
        user_details = self.user_id_by_session_id.get(session_id)
        if user_details is None:
            return None
        if "created_at" not in user_details.keys():
            return None
        if self.session_duration <= 0:
            return user_details.get("user_id")
        created_at = user_details.get("created_at")
        allowed_window = created_at + timedelta(seconds=self.session_duration)
        if allowed_window < datetime.now():
            return None
        return user_details.get("user_id")
