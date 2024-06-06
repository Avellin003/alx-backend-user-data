#!/usr/bin/env python3
"""the module for the Session Authorization protocol"""
import base64
from uuid import uuid4
from typing import TypeVar

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Session Authorization class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creation of a session ID
        arguments:
            users_id (str): user's user id
        returns:
            - the session ID created
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        id = uuid4()
        self.user_id_by_session_id[str(id)] = user_id
        return str(id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a User ID based on a Session ID
        arguments:
            session_id (str): the session ID
        returns:
            the user ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        returns a User instance based on a cookie value
        arguments:
            request : request object
        returns:
            the instance
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
