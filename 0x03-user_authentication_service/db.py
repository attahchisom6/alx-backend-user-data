#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar

from user import Base, User


class DB:
    """
    storage class
    """
    def __init__(self): -> None:
        """
        inittializing storage engine
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)

        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self._session = sessionmaker()

    @property
    def _session(self) -> session:
        """
        a getter method to return a session
        """
        if self._session is None:
