#!/usr/bin/env python3
"""
SessionDBAuth class definition
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class that stores session data in a database
    """

    def create_session(self, user_id=None):
        """
        Generates a Session ID for a user_id
        """
        sessionid = super().create_session(user_id)
        if not sessionid:
            return None
        kw = {
            "user_id": user_id,
            "session_id": sessionid
        }
        user = UserSession(**kw)
        user.save()
        return sessionid

    def user_id_for_session_id(self, session_id=None):
        """
        Gets a user ID from a session ID
        """
        userid = UserSession.search({"session_id": session_id})
        if userid:
            return userid
        return None

    def destroy_session(self, request=None):
        """
        Removes a UserSession instance using a Session ID from a request cookie
        """
        if request is None:
            return False
        sessionid = self.session_cookie(request)
        if not sessionid:
            return False
        user_session = UserSession.search({"session_id": sessionid})
        if user_session:
            user_session[0].remove()
            return True
        return False
