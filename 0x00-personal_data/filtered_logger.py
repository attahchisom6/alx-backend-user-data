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


class RedactionFormatter(logging.Formatter):
    """
    redaction formatter class
    """
    REDACTION = "***"
    FORMAT = "[Holberton] %(name) %(levelname) %(asctime)s - 15s: %(message)s"

    def __init__(self):
        """
        object factory: generating redaction object
        """
        super(RedactionFormatter, self).__init__(self)

    def format(record: logging.Lo
