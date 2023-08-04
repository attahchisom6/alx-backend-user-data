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
""" Personal data project """
from typing import List
import re
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


<<<<<<< HEAD
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
def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """ returns the log message obfuscated """
    for i in fields:
        message = re.sub(fr'{i}=.+?{separator}',
                         f'{i}={redaction}{separator}', message)
    return message


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

        """ constructor method """

        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        method to filter values in incoming log records using filter_datum
        """
        return filter_datum(
                self.fields,
                self.REDACTION,
                super().format(record),
                self.SEPARATOR)
        """ filter values in a log record"""
        return filter_datum(self.fields,
                            self.REDACTION,
                            super().format(record),
                            self.SEPARATOR


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

    cursor.close()
    connector.close()
    """ return logging.Logger object """
    obj = logging.getLogger("user_data")
    obj.setLevel(logging.INFO)
    obj.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    obj.addHandler(handler)
    return obj


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ return the connector of the database """
    user_name = os.getenv('PERSONAL_DATA_DB_USERNAME')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    return mysql.connector.connect(user=user_name,
                                   password=password,
                                   host=host,
                                   database=db_name)


def main():
    """ main function """
    conn = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * from users")
    fields = [user[0] for user in cursor.description]
    print(fields)

    logger = get_logger()

    for i in cursor:
        list_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(i, fields))
        logger.info(i)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()`
