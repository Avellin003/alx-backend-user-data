#!/usr/bin/env python3
"""filter_datum definition"""
import re


def filter_datum(fields, redaction, message, separator) -> str:
    """returns the log message obfuscated with redaction
    Args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating all
        fields in the log line"""
    return re.sub(separator.join(fields), redaction, message)
