#!/usr/bin/env python3
"""filter_datum definition"""
import re


def filter_datum(fields, redaction, message, separator) -> str:
    """returns the log message obfuscated"""
    return re.sub(separator.join(fields), redaction, message)
