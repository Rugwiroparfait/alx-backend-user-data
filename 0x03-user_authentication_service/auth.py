#!/usr/bin/env python3
"""
Auth module
"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


class Auth:
    """ Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hashes a password using bcrypt's hashpswd function
        with a generated salt

        Args:
            password (str): The password to be hashed

        Returns:
            bytes: The hashed password in bytes
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)

        return hashed_password

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with email and password.

        Args:
            email (str): The user's email
            password (str): The user's password
        Returns:
            User: The created user

        Raises:
            ValueError: If the user already exists
        """
        try:
            # check if the user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If the user does not exist, create a new one
            hashed_password = self._hash_password(password)
            user = self._db.add_user(email, hashed_password.decode())
            return user
