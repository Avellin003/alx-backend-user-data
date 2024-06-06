#!/usr/bin/env python3
"""the default auth module"""
import os
from flask import request
from typing import (
    List,
    TypeVar
)


class Auth:
    """Auth class for the default auth module"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        determine if a path requires authentication
        arguments:
            - path(str): url path
            - excluded_paths(List of str): list of paths that do not require
        returns:
            - true if path requires authentication, false otherwise
        """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns the value of the Authorization header in the request"""
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None - not implemented"""
        return None

    def session_cookie(self, request=None):
        """
        returns the value of the session cookie from a request
        arguments:
            requests : requests the object
        returns:
            - the value of the session cookie
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
