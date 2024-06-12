#!/usr/bin/env bash
"""
User model for the user authentication service
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
# declarative_base is in charge of tables in the database
"""Making an instance of the Base class"""
Base = declarative_base()


class User(Base):
    """User class for the user authentication service"""
    # the __tablename__ attribute defines the name of the table
    __tablename__ = 'users'

    # the id attribute is a column of the table
    # it is an integer and can not be null nor repeated (primary_key)
    id = Column(Integer, primary_key=True)
    # the email attribute is a column of the table
    # it is a string, can not be empty
    email = Column(String(250), nullable=False)
    # the hashed_password attribute is a column of the table
    # it is a string, can not be empty
    hashed_password = Column(String(250), nullable=False)
    # the session_id attribute is a column of the table
    # it is a string, can be empty
    session_id = Column(String(250), nullable=True)
    # the reset_token attribute is a column of the table
    # it is a string, can be empty
    reset_token = Column(String(250), nullable=True)
