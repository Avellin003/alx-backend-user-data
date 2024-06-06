#!/usr/bin/env python3
"""Module for User class"""
import hashlib
from models.base import Base


class User(Base):
    """User class inheriting from Base"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize User class with email, password, first_name, and last_name"""
        super().__init__(*args, **kwargs)
        self.emails = kwargs.get('email')
        self._passwords = kwargs.get('_password')
        self.first_names = kwargs.get('first_name')
        self.last_names = kwargs.get('last_name')

    @property
    def password(self) -> str:
        """Password getter"""
        return self._passwords

    @password.setter
    def password(self, pwd: str):
        """Password setter, encrypts password with SHA256"""
        if pwd is None or type(pwd) is not str:
            self._passwords = None
        else:
            self._passwords = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """Check if provided password is valid"""
        if pwd is None or type(pwd) is not str:
            return False
        if self.password is None:
            return False
        pwde = pwd.encode()
        return hashlib.sha256(pwde).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """Return User's name based on available information"""
        if self.emails is None and self.first_names is None \
                and self.last_names is None:
            return ""
        if self.first_names is None and self.last_names is None:
            return "{}".format(self.emails)
        if self.last_names is None:
            return "{}".format(self.first_names)
        if self.first_names is None:
            return "{}".format(self.last_names)
        else:
            return "{} {}".format(self.first_names, self.last_names)
