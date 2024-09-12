#!/usr/bin/env python3
"""
filtered_logger.py - A module for filtering and obfuscating/
sensitive information.
"""

import re
import logging
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Obfuscate the value of sensitive fields in a log message.

    Args:
        fields (List[str]): Fields to obfuscate.
        redaction (str): Redaction string to replace field values.
        message (str): The original log message.
        separator (str): Separator character between fields in the log.

    Returns:
        str: Obfuscated log message.
    """
    for field in fields:
        message = re.sub(
            f"{field}=[^{separator}]*",
            f"{field}={redaction}",
            message
        )
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with fields to obfuscate.

        Args:
            fields (List[str]): Fields to obfuscate in the log message.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record by obfuscating sensitive fields.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log record with sensitive fields obfuscated.
        """
        original_message = super(RedactingFormatter, self).format(record)
        return filter_datum(
            self.fields, self.REDACTION, original_message, self.SEPARATOR
            )
