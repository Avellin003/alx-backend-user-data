#!/usr/bin/env python3
"""
Definition of password hashing and utility functions
"""
import bcrypt
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from typing import (
    TypeVar,
    Union
)

from db import DB
from user import User

U = TypeVar(User)

def _hash_password(password: str) -> bytes:
    """
    Encrypt a password string and return it in byte format.
    Args:
        password (str): password in plain text
    """
    pwd_bytes = password.encode('utf-8')
    return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())

def _generate_uuid() -> str:
    """
    Generate a UUID and return its string representation.
    """
    return str(uuid4())

class Auth:
    """Auth class to manage authentication and user sessions.
    """

    def __init__(self) -> None:
        self._database = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user and return the user object.
        Args:
            email (str): email address of the new user
            password (str): password for the new user
        Return:
            If no user with the given email exists, return the newly created user
            Else raise a ValueError
        """
        try:
            self._database.find_user_by(email=email)
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            user_obj = self._database.add_user(email, hashed_pwd)
            return user_obj
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's login credentials and return True if they are correct,
        otherwise return False.
        Args:
            email (str): user's email address
            password (str): user's password
        Return:
            True if credentials are correct, otherwise False
        """
        try:
            user_obj = self._database.find_user_by(email=email)
        except NoResultFound:
            return False

        stored_hashed_password = user_obj.hashed_password
        pwd_bytes = password.encode("utf-8")
        return bcrypt.checkpw(pwd_bytes, stored_hashed_password)

    def create_session(self, email: str) -> Union[None, str]:
        """
        Create a session ID for an existing user and update the user's
        session_id attribute.
        Args:
            email (str): user's email address
        """
        try:
            user_obj = self._database.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id_str = _generate_uuid()
        self._database.update_user(user_obj.id, session_id=session_id_str)
        return session_id_str

    def get_user_from_session_id(self, session_id: str) -> Union[None, U]:
        """
        Retrieve the user associated with a given session_id, if one exists,
        otherwise return None.
        Args:
            session_id (str): session ID for the user
        Return:
            User object if found, otherwise None
        """
        if session_id is None:
            return None

        try:
            user_obj = self._database.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user_obj

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a user's session by updating their session_id attribute to None.
        Args:
            user_id (int): ID of the user
        Return:
            None
        """
        try:
            self._database.update_user(user_id, session_id=None)
        except ValueError:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset token UUID for a user identified by the given email.
        Args:
            email (str): user's email address
        Return:
            Newly generated reset_token for the user
        """
        try:
            user_obj = self._database.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token_str = _generate_uuid()
        self._database.update_user(user_obj.id, reset_token=reset_token_str)
        return reset_token_str

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update a user's password using the provided reset token.
        Args:
            reset_token (str): reset token issued for password reset
            password (str): new password for the user
        Return:
            None
        """
        try:
            user_obj = self._database.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()

        new_hashed_password = _hash_password(password)
        self._database.update_user(user_obj.id, hashed_password=new_hashed_password, reset_token=None)
