#!/usr/bin/env python3
""" Module of session AUthenntication
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Session authentication class that inherits from Auth """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session ID for a given user_id.
        - Return None if user_id is None or not a string.
        - Generate a session ID using uuid4 and store it in the dictionary.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a unique session ID using uuid4
        session_id = str(uuid.uuid4())

        # Store session_id and user_id in the dictionary
        self.user_id_by_session_id[session_id] = user_id

        # Return the generated session ID
        return session_id
