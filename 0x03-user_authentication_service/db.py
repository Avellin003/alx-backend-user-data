#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db",
                                     echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Makes a User object and save it to database
        Arguments:
            email (string): user email address
            hashed_password(string): password hashed by bcrypt's hashpw
        returns:
            Newly created User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        fetches the user who has an attribute matching the attributes passed
        as arguments
        Arguments:
            atts (dictionary): a dictionary of attributes to match the user
        Returns:
            matching user or raise error
        """
        all_users = self._session.query(User)
        for o, w in kwargs.items():
            if o not in User.__dict__:
                raise InvalidRequestError
            for us in all_users:
                if getattr(us, o) == w:
                    return us
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        updates the attributes
        Argus:
            user_id (integer): user's id
            kwargs (dict): dictionary of attributes to update
        Returns:
            No return
        """
        try:
            us = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError()
        for o, w in kwargs.items():
            if hasattr(us, o):
                setattr(us, o, w)
            else:
                raise ValueError
        self._session.commit()
