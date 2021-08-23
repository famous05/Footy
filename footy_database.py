# footy_database.py
#!/usr/bin/env python3

""" Python script to interact with Footy.db sqlite database

Available functions:
    - create_connection
    - drop_table
    - check_table_exist
    - get_table_names
    - get_database_name
...
"""

import sqlite3
from sqlite3 import Error
import os

db_name = os.getcwd() + "/Footy.db"

def create_connection():
    """ Create a database connection to the SQLite database. 
    
    Args:
        db_file:   SQLite3 database to connect to

    Returns:
        Connection object or None
    """
    connection = None
    try:
        connection = sqlite3.connect(db_name)
        return connection
    except Error as e:
        print(e)

    return connection


def drop_table(connection, table_name):
    """ Drop the tabler 'table_name' from database
    
    Args:
        connection:   Connection object
        table_name:   Name of table to drop

    Returns:
    """

    c = connection.cursor()
    c.execute(" DROP TABLE " + table_name + ";")


def table_exist(connection, table_name):
    """ Check if a table exist in a database
    
    Args:
        connection:     Connection object
        table_name:     Name of table

    Returns:
        True or False
    """
    c = connection.cursor()
                
    # Get the count of tables with the name
    sql_cmd =" SELECT count(name) FROM sqlite_master WHERE type='table' AND name=" + "'" + table_name + "'"
    c.execute(sql_cmd)

    # If the count is 1, then table exists
    if c.fetchone()[0] == 1:
        return True
    return False


def get_table_names(connection):
    """ Get names of all table in the database
    
    Args:
        connection:     Connection object

    Returns:
        Names of all tables
    """
    c = connection.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return c.fetchall()


def get_database_name():
    """ Returns the name of the database. """
    return db_name
