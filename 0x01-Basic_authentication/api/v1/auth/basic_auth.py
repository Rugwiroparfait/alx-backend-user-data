#!/usr/bin/env python3
""" implements Basic Auth """

from api.v1.auth.auth import Auth
from models.user import User
import re
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic Auth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extracts Base64 part of Authorization header"""
        if authorization_header is None or\
                not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split("Basic ")[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes Base64 string """
        if base64_authorization_header is None or\
                not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_bytes = base64_authorization_header.encode("utf-8")
            data_bytes = base64.b64decode(base64_bytes)
            return data_bytes.decode("utf-8")
        except (UnicodeDecodeError, base64.binascii.Error):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ returns user email and password from base64 decoded value"""
        if decoded_base64_authorization_header is None or\
                not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ decodes users credentials """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        user_list = User.search({'email': user_email})
        if len(user_list) == 0:
            return None
        user = user_list[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user
