#!/usr/bin/env python3
"""
create a filter, a filter provides a fine grained
fgacility that determines where the log output
its content
"""
import re
import logging
from typing import List


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
    FORMAT = "[HOLBERTON] %(name) %(levelname) %(asctime)s-15s: %(message)s"
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
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)
