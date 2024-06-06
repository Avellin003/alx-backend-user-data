#!/usr/bin/env python3
"""
SessionAuth class definition
"""
import base64
from uuid import uuid4
from typing import TypeVar

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ Session Authorization protocol methods implementation
    """
    usersession_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Generates a Session ID for a user with id user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        ids = uuid4()
        self.usersession_id[str(ids)] = user_id
        return str(ids)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Gets a user ID from a session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.usersession_id.get(session_id)

    def current_user(self, request=None):
        """
        Gets a user instance using a cookie value
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """
        Removes a user session
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.usersession_id[session_cookie]
        return True
