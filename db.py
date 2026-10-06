"""MySQL connection helpers."""

import os
from pathlib import Path

import mysql.connector
from mysql.connector import MySQLConnection

BASE_DIR = Path(__file__).resolve().parent
MYSQL_HOST = ""
MYSQL_PORT = ""
MYSQL_USER = ""
MYSQL_PASSWORD = ""
MYSQL_DATABASE = ""


def get_connection() -> MySQLConnection:
    """Connect using MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE."""
    if not MYSQL_HOST:
            raise ValueError("MYSQL_HOST is not set.")
    
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
    )