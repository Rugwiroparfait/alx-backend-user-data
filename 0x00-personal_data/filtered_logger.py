#!/usr/bin/env python3
"""
filtered_logger.py - A module for filtering and obfuscating
sensitive information.
"""

import re
import logging
from typing import List, Tuple
import os
import mysql.connector
from mysql.connector import connection, MySQLConnection

# PII fields to obfuscate
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


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

    REDACTION: str = "***"
    FORMAT: str = (
        "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    )

    SEPARATOR: str = ";"

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


def get_logger() -> logging.Logger:
    """
    Returns a logger object with a custom redacting formatter.

    The logger is named 'user_data', logs messages up to INFO level,
    and uses the RedactingFormatter to obfuscate PII.

    Returns:
        logging.Logger: A configured logger object.
    """
    logger: logging.Logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False  # Do not propagate logs to other loggers

    # Create a StreamHandler with RedactingFormatter
    handler: logging.StreamHandler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


def get_db() -> MySQLConnection:
    """
    Connect to a secure MySQL database using credentials from
    environment variables and return a MySQL connection object.

    Environment Variables:
        PERSONAL_DATA_DB_USERNAME: Database username.
        PERSONAL_DATA_DB_PASSWORD: Database password.
        PERSONAL_DATA_DB_HOST: Database host.
        PERSONAL_DATA_DB_NAME: Database name.

    Returns:
        MySQLConnection: A connector to the database.
    """
    username: str = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password: str = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host: str = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name: str = os.getenv('PERSONAL_DATA_DB_NAME')

    # Connect to the database using mysql-connector
    connection: MySQLConnection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )

    return connection


def main() -> None:
    """
    Main function that connects to the database and retrieves
    and logs all rows in the 'users' table with sensitive data obfuscated.
    """
    db: MySQLConnection = get_db()
    cursor = db.cursor()

    # Query to select all rows from the users table
    cursor.execute(
        """
        SELECT name, email, phone, ssn, password, ip, last_login, user_agent
        FROM users;
        """
    )

    # Create a logger
    logger: logging.Logger = get_logger()

    # Fetch and log each row with obfuscation
    for row in cursor:
        log_message = (
            f"name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]}; "
            f"password={row[4]}; ip={row[5]}; last_login={row[6]}; "
            f"user_agent={row[7]};"
        )

        logger.info(log_message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
