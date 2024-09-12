#!/usr/bin/env python3
"""
filtered_logger.py - A module for filtering and obfuscating sensitive.
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscate the value of sensitive fields in a long message.
    
    Args:
        fields (List[str]): fields to obfuscate.
        redaction (str): Redaction string to replace field values.
        message (str): The original log message.
        separator (str): Separator character between fields in the log.
    
    Returns:
        str: Obfuscated log message.
    """
    for field in fields:
        message = re.sub(f"{field}=[^{separator}]*", f"{field}={redaction}", message)
    return message
