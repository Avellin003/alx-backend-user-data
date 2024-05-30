#!/usr/bin/env python3
"""
filter_logger module that obfuscates fields in a log message
"""
import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    for i in fields:
        sms = re.sub(i + '=' + '.*?' + separator,
                     i + '=' + redaction + separator, message)
    return sms


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class that inherits from logging.Formatter"""

    REDACTION = "***"
    FORMAT = ("[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: "
              "%(message)s")
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Redacting Formatter constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum
        args: record: log record
        """
        sms = super(RedactingFormatter, self).format(record)
        red = filter_datum(self.fields, self.REDACTION, sms, self.SEPARATOR)
        return red


def get_logger() -> logging.Logger:
    """
    definition that takes no arguments and returns a logging.Logger object
    """
    log = logging.getLogger("user_data")
    log.setLevel(logging.INFO)
    log.propagate = False

    handler = logging.StreamHandler()

    formatter = RedactingFormatter(PII_FIELDS)

    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', "root")
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', "")
    host = os.getenv('PERSONAL_DATA_DB_HOST', "localhost")
    database_name = os.getenv('PERSONAL_DATA_DB_NAME')
    conector = mysql.connector.connect(
        user=user,
        password=passwd,
        host=host,
        database=database_name
    )
    return conector


def main():
    """reads and retrieves all rows in the users table"""
    database = get_db()
    log = get_logger()
    cursor = database.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for row in cursor:
        message = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        log.info(message.strip())
    cursor.close()
    database.close()


if __name__ == "__main__":
    main()
