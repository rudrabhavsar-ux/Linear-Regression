import sqlite3
import os

# Absolute path anchored to this file's own location, so it resolves
# to the same database no matter where the calling script is run from.
DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Personal.db")


def get_connection():
    con = sqlite3.connect(DB_NAME)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con
