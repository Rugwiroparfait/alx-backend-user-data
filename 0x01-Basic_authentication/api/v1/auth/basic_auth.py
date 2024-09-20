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

    def decode_base64_authorization_header(self,
                                            base64_authorization_header: str) -> str:
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
