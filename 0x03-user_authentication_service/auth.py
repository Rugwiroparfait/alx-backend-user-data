#!/usr/bin/env python3
"""
Auth module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt's hashpw function
    with a generated salt

    Args:
        password (str): The password to be hashed

    Returns:
        bytes: The hashed password in bytes
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password
