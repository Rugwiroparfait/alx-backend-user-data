#!/usr/bin/env python3
""" implements Basic Auth """

from api.v1.auth.auth import Auth
from models.user import User
import re
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic Auth class"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ Extracts Base64 part of Authorization header"""
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split("Basic ")[1]
