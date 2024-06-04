#!/usr/bin/env python3
"""
Module for Basic Authorization
"""
import base64
from .auth import Auth
from typing import TypeVar

from models.user import User


class BasicAuth(Auth):
    """Performs Basic Authorization
    and returns the User instance based on the Authorization header
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Gets the Base64-encoded value of the Authorization header
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
        Decrypted Base64 value of the Authorization header
        and returns the decoded value
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            text = base64_authorization_header.encode('utf-8')
            text = base64.b64decode(text)
            return text.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> tuple[str, str]:
        """
        return the email and password from the Base64 decoded value
        and returns a tuple of the email and password
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email = decoded_base64_authorization_header.split(":")[0]
        password = decoded_base64_authorization_header[len(email) + 1:]
        return (email, password)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance based on email and password
        and returns the User instance based on the email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for u in users:
                if u.is_valid_password(user_pwd):
                    return u
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> User:
        """
        return the User instance based on the Authorization header
        and returns None if the User is not found
        """
        Auth_header = self.authorization_header(request)
        if Auth_header is not None:
            token = self.extract_base64_authorization_header(Auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, pword = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, pword)
        return
