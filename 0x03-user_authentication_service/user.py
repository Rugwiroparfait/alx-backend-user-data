#!/usr/bin/env python3
"""
This module defines the user model for the database
"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class User(Base):
    """
    User model representinf a record in the users table/

    Atrributes:
        id (int) : the unique identifier for the user (primary key).
        email (str) : The user's email address (non-nullable).
        hashed_password (str): The hashed password for the user (non-nullable).
        session_id (str): The session identifier for the User (nullable).
        reset_token (str): The token for password reset (nullable).
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
