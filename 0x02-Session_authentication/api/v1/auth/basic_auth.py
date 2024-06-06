#!/usr/bin/env python3
"""
BasicAuth class definition
"""
import base64
from .auth import Auth
from typing import TypeVar

from models.user import User


class BasicAuth(Auth):
    """ Basic Authorization protocol methods implementation
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Gets the Base64 part of the Basic Authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        tok = authorization_header.split(" ")[-1]
        return tok

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        Decodes a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            txt = base64_authorization_header.encode('utf-8')
            txt = base64.b64decode(txt)
            return txt.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Gets user email and password from decoded Base64 value
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        emails = decoded_base64_authorization_header.split(":")[0]
        passwords = decoded_base64_authorization_header[len(emails) + 1:]
        return (emails, passwords)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Gets a User instance using email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for a in users:
                if a.is_valid_password(user_pwd):
                    return a
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Gets a User instance from a request
        """
        Authheader = self.authorization_header(request)
        if Authheader is not None:
            tok = self.extract_base64_authorization_header(Authheader)
            if tok is not None:
                txt = self.decode_base64_authorization_header(tok)
                if txt is not None:
                    email, pwords = self.extract_user_credentials(txt)
                    if email is not None:
                        return self.user_object_from_credentials(email, pwords)
        return
