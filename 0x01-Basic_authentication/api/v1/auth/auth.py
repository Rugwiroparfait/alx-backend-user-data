#!/usr/bin/env python3
""" creating auth  class to manage the API authentication """
from flask import request
from typing import List, TypeVar
from models.user import User


class Auth:
    """ The Auth class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ return False """
        return False

    def authorization_header(self, request=None) -> str:
        """ return None """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Return None. """
        return None
