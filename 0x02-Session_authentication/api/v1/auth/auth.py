#!/usr/bin/env python3
"""
Auth class definition
"""
import os
from flask import request
from typing import (
    List,
    TypeVar
)


class Auth:
    """
    API authentication management
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if a path requires authentication
        Args:
            - path(str): Url path
            - excluded_paths(List of str): Paths not requiring authentication
        Return:
            - True if path requires authentication, else False
        """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for a in excluded_paths:
                if a.startswith(path):
                    return False
                if path.startswith(a):
                    return False
                if a[-1] == "*":
                    if path.startswith(a[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Gets the authorization header from a request
        """
        if request is None:
            return None
        head = request.headers.get('Authorization')
        if head is None:
            return None
        return head

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Gets a User instance from a request
        """
        return None

    def session_cookie(self, request=None):
        """
        Gets a cookie from a request
        Args:
            request : request object
        Return:
            _my_session_id cookie value from request
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
