#!/usr/bin/env python3
""" creating auth  class to manage the API authentication """
from flask import request
from typing import List, TypeVar
from models.user import User


class Auth:
    """ The Auth class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ True  if path is not in the list of strings
            excluded_paths
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != "/":
            path += '/'
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """ Implement request validation and ensure that/
            only authenticated users can access certain routes.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Return None. """
        return None
