#!/usr/bin/env python3
"""Users module"""
import os
from flask import request
from typing import (
    List,
    TypeVar
)


class Auth:
    """Deals with authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        checks
        argumnets:
            - paths(str): Url to check
            - excluded_pat: list not to check
        Returns:
            - The True if path is not in excluded_paths, else False
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
                if path.startswith(i):
                    return False
                if a[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns the value of the Authorization header in the request"""
        if request is None:
            return None
        head = request.headers.get('Authorization')
        if head is None:
            return None
        return head

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the User instance based on a cookie value"""
        return None

    def session_cookie(self, request=None):
        """
        return a cookie from a request
        arguments:
            requests : request object
        returns:
            values of the cookie
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
