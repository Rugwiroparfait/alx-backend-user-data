#!/usr/bin/env python3
"""
Auth module
"""
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


class Auth:
    """ Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates credentials: email and password
        Returbs True if valid, otherwise False
        """
        try:
            # Locate user by email
            user = self._db.find_user_by(email=email)
            # Check if the provided password matches the stored hashed password
            is_valid = bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.hashed_password.encode('utf-8')
            )
            return is_valid
        except Exception:
            return False

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

    def _generate_uuid(self) -> str:
        """generate a new uuid and returns its string represantation."""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Creates a session ID for the user and stores it in the database.

        Args:
            email (str): The user's email.

        Returns:
            str: The session ID if the user is found, otherwise None.
        """
        try:
            # Locate the user by email
            user = self._db.find_user_by(email=email)
            # Generate a new session ID using the _generate_uuid method
            session_id = self._generate_uuid()
            # Update the user's session ID in the database
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
