#!/usr/bin/env python3
"""
create a filter, a filter provides a fine grained
fgacility that determines where the log output
its content
"""
from typing import List


def filtered_logger(field: List, redaction: str):
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
