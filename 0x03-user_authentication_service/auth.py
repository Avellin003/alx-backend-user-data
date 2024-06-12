#!/usr/bin/env python3
"""
Definition of utility functions and Auth class
"""
import bcrypt
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar, Union
from db import DB
from user import User

U = TypeVar('User')


def _hash_password(password: str) -> bytes:
    """
    Encrypt a password string and return the encrypted password as bytes.
    Args:
        password (str): the password in string format.
    """
    encoded_password = password.encode('utf-8')
    return bcrypt.hashpw(encoded_password, bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generate a new UUID and return its string representation.
    """
    return str(uuid4())


class Auth:
    """Auth class for handling user authentication operations."""

    def __init__(self) -> None:
        self._db_instance = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user and return a user object.
        Args:
            email (str): the new user's email address.
            password (str): the new user's password.
        Return:
            The newly created user object.
        """
        try:
            self._db_instance.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db_instance.add_user(email, hashed_password)
            return new_user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's login credentials.
        Args:
            email (str): the user's email address.
            password (str): the user's password.
        Return:
            True if the credentials are correct, else False.
        """
        try:
            user = self._db_instance.find_user_by(email=email)
        except NoResultFound:
            return False

        user_hashed_password = user.hashed_password
        encoded_password = password.encode("utf-8")
        return bcrypt.checkpw(encoded_password, user_hashed_password)

    def create_session(self, email: str) -> Union[None, str]:
        """
        Create a session_id for an existing user and update the user's
        session_id attribute.
        Args:
            email (str): the user's email address.
        Return:
            The session_id if user is found, else None.
        """
        try:
            user = self._db_instance.find_user_by(email=email)
        except NoResultFound:
            return None

        new_session_id = _generate_uuid()
        self._db_instance.update_user(user.id, session_id=new_session_id)
        return new_session_id

    def get_user_from_session_id(self, session_id: str) -> Union[None, U]:
        """
        Retrieve a user by session_id, if one exists, else return None.
        Args:
            session_id (str): the session id for user.
        Return:
            The user object if found, else None.
        """
        if session_id is None:
            return None

        try:
            user = self._db_instance.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
        destroy a user's session by setting the session_id to None.
        Args:
            user_id (int): the user's id.
        Return:
            None
        """
        try:
            self._db_instance.update_user(user_id, session_id=None)
        except ValueError:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset_token for a user identified by the given email.
        Args:
            email (str): the user's email address.
        Return:
            The newly generated reset_token for the relevant user.
        """
        try:
            user = self._db_instance.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        new_reset_token = _generate_uuid()
        self._db_instance.update_user(user.id, reset_token=new_reset_token)
        return new_reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update a user's password.
        Args:
            reset_token (str): the reset_token issued to reset the password.
            password (str): the user's new password.
        Return:
            None
        """
        try:
            user = self._db_instance.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()

        hashed_password = _hash_password(password)
        hp = hashed_password
        self._db_instance.update_user(
            user.id,
            hashed_password=hp,
            reset_token=None
        )
