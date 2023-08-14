#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound, InvalidRequestError, MultipleResultsFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """
    storage class
    """
    def __init__(self) -> None:
        """
        inittializing storage engine
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)

        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        a getter method to return a session
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        add and saves a user to the database
        """
        db = self._session
        new_user = User(email=email, hashed_password=hashed_password)

        db.add(new_user)
        db.commit()

        return new_user

    def find_user_by(self, **kwargs: dict) -> User:
        """
        search the user table and returns the user in the first row whose
        attribute mathes key-values in kwargs
        Args:
            kwargs: the search parameter
        Return: the user
        """
        # a property method is called without a parenthesis
        db = self._session
        try:
            users = db.query(User)
            user = users.filter_by(**kwargs)
            return user
        except Exception:
            raise NoResultFound
        except MutipleResultFound:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs: dict) -> None:
        """
        method that locates a user and updates a its attribute
        """
        db = self._session
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if not hasattr(user, key):
                    raise ValueError
                setattr(user, key, value)
            db.commit()
        except Exception:
            pass
