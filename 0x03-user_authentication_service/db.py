#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User

class DB:
    """DB class for interacting with the database
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__db_session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__db_session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__db_session = DBSession()
        return self.__db_session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a user to the database and returns the User object

        Args:
            email (str): The email of the user
            hashed_password (str): The hashed passord of the user

        Returns:
            User: The newly created User Object
        """
        # Create a newly created User object
        new_user = User(email=email, hashed_password=hashed_password)

        # Add the user to the session and commit the transaction
        self._session.add(new_user)
        self._session.commit()

        # Return the new created user
        return new_user
