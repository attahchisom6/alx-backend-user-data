#!/usr/bin/env python3
"""
create a filter, a filter provides a fine grained
fgacility that determines where the log output
its content
"""
import re
import logging
from typing import List
from os import getenv
from mysql.connector import connection


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str], redaction: str, message: str,
        separator: str) -> str:
    """
    function to obfuscate/hide relevant information
    of a field
    Args:
        field: list of strings representing all
        field to obfuscate
        redaction: a string representing by what the
        string will be obfuscated
        message: a string representing the log line
        separator: a string representing by which the field
        in the log line are delimited in the log line (message)
    """
    field_pattern = "|".join(fields)
    line_pattern = r"({})=[^{}]*".format(field_pattern, separator)
    re_daction = r"\1={}".format(redaction)
    return re.sub(line_pattern, re_daction, message)


class RedactingFormatter(logging.Formatter):
    """
    redaction formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)s-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        object factory: generating redaction object
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        method to filter values in incoming log records using filter_datum
        """
        return filter_datum(
                self.fields,
                self.REDACTION,
                super().format(record),
                self.SEPARATOR)


# This a function not a method
def get_logger() -> logging.Logger:
    """
    A function that takes no argument but returns a login.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = RedactingFormatter(PII_FIELDS)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """
    function that returns a connector to the database
    """
    # note: os.getenv does the same thing
    username = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = getenv("PERSONAL_DATA_DB_NAME")

    connector = connection.MySQLConnection(
            user=username,
            password=password,
            database=db_name,
            host=db_host
        )
    return connector


def main():
    """
    function to get rows from the user table and display
    them to the console
    """
    connector = get_db()
    cursor = connector.cursor()
    logger = get_logger()

    query = "SELECT * FROM users"
    cursor.execute(query)
    all_rows = cursor.fetchall()

    for row in all_rows:
        field_1 = "name={}, email={}, phone={}, ssn={}, "
        field_2 = "password={}, ip={}, last_login={}, user_agent={}"
        fields = field_1 + field_2
        fields = fields.format(
                row[0], row[1], row[2], row[3],
                row[4], row[5], row[6], row[7])
        logger.info(fields)


if __name__ == "__main__":
    main()
