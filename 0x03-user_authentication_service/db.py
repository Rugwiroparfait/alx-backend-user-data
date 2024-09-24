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

        """Adds a user to the database and returns the User object.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds user by arbitrary keyword arguments
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No User found")
        except InvalidRequestError:
            raise InvalidRequestError("Invalied query")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes and commits the change to the database

        Args:
            user_id (int): The ID of the user to update
            kwargs: Arbitrary keyword arguments representing
                    attributes to update

        Raises:
            ValueError: If any of the keyword arguments do
            not match a User attribute
        """
        # Find the user by Id
        user = self.find_user_by(id=user_id)

        # Update user attributes
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"{key} \
                                is not a valid attribute of User")
            setattr(user, key, value)

        # Commit the updated values to the database
        self._session.commit()
