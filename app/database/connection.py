import sqlite3

DATABASE_NAME = "expense_tracker.db"

def get_connection():

    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def get_db():

    Connection = get_connection()

    try:
        yield Connection

    finally:
        Connection.close()