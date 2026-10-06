"""MySQL connection and DB functions."""

import os

import mysql.connector
from mysql.connector import MySQLConnection

MYSQL_HOST = os.getenv("MYSQLHOST")
MYSQL_PORT = int(os.getenv("MYSQLPORT", "3306"))
MYSQL_USER = os.environ["MYSQLUSER"]
MYSQL_PASSWORD = os.environ["MYSQLPASSWORD"]
MYSQL_DATABASE = os.environ["MYSQLDATABASE"]


def get_connection() -> MySQLConnection:
    """Connect using MYSQLHOST, MYSQLPORT, MYSQLUSER, MYSQLPASSWORD, MYSQLDATABASE."""
    if not MYSQL_HOST:
            raise ValueError("MYSQL_HOST is not set.")
    
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
    )