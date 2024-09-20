#!/usr/bin/env python3
""" implements Basic Auth """

from api.v1.auth.auth import Auth
from models.user import User
import re
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic Auth class"""
    pass
