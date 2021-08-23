# footy_database_stadiums.py
#!/usr/bin/env python3

""" Python script to interact with stadiums tables in Footy.db sqlite database

Available functions:
    - create_connection
    - create_present_stadiums_table
    - create_past_stadiums_table
    - add_present_stadium
    - add_past_stadium
    - get_all_present_stadiums
    - get_all_past_stadiums

...
"""

import os, sys
import sqlite3
from sqlite3 import Error

# Add parent directory to sys.path
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import footy_database


# Setup SQL commands
CREATE_PRESENT_STADIUMS_TABLE = "CREATE TABLE IF NOT EXISTS present_stadiums (id INTEGER PRIMARY KEY, city TEXT, club TEXT, stadium_name TEXT, capacity INTEGER, country TEXT);"

CREATE_PAST_STADIUMS_TABLE = "CREATE TABLE IF NOT EXISTS past_stadiums (id INTEGER PRIMARY KEY, club TEXT, past_stadium_name TEXT, year_closed INTEGER);"

INSERT_PRESENT_STADIUM = "INSERT INTO present_stadiums (city, club, stadium_name, capacity, country) VALUES (?, ?, ?, ?, ?);"            

INSERT_PAST_STADIUM = "INSERT INTO past_stadiums (club, past_stadium_name, year_closed) VALUES (?, ?, ?);"            

GET_ALL_PRESENT_STADIUMS = "SELECT * FROM present_stadiums;"

GET_ALL_PAST_STADIUMS = "SELECT * FROM past_stadiums;"

GET_CLUB_PAST_STADIUM_NAME = """
SELECT past_stadium_name FROM past_stadiums
WHERE club = ? AND year_closed >= ?
LIMIT 1;
"""

GET_CLUB_PRESENT_STADIUM_NAME = """
SELECT stadium_name FROM present_stadiums
WHERE club = ?
LIMIT 1;
"""


def create_present_stadiums_table(connection):
    """ Create 'present_stadium' table in the database. 
    
    Args:
        connection:   Connection object

    Returns:
    """

    try:
        if present_stadiums_table_exist(connection):
            drop_present_stadiums_table(connection)
        c = connection.cursor()
        c.execute(CREATE_PRESENT_STADIUMS_TABLE)
    except Error as e:
        print(e)


def create_past_stadiums_table(connection):
    """ Create 'past_stadium' table in the database. 
    
    Args:
        connection:   Connection object

    Returns:
    """

    try:
        if past_stadiums_table_exist(connection):
            drop_past_stadiums_table(connection)
        c = connection.cursor()
        c.execute(CREATE_PAST_STADIUMS_TABLE)
    except Error as e:
        print(e)


def add_present_stadium(connection, city, club, stadium_name, capacity, country):
    """ Add a record to the 'present_stadiums' table 
    
    Args:
        connection:     Connection object
        city:           City
        club:           Club
        stadium_name:   Stadium name
        capacity:       Capacity e.g 23000
        country:        Country of club e.g England

    Returns:
        Not applicable
    """
    with connection:
        connection.execute(INSERT_PRESENT_STADIUM, (city, club, stadium_name, capacity, country))


def add_past_stadium(connection, club, past_stadium_name, year_closed):
    """ Add a record to the 'past_stadiums' table 
    
    Args:
        connection:         Connection object
        past_stadium_name:  Past stadium name
        year_closed:        Year closed e.g 1999

    Returns:
    """
    with connection:
        connection.execute(INSERT_PAST_STADIUM, (club, past_stadium_name, year_closed))


def get_all_present_stadiums(connection):
    """ Get all records in the 'present_stadiums' table 
    
    Args:
        connection:   Connection object

    Returns:
        All records in table
    """
    with connection:
        return connection.execute(GET_ALL_PRESENT_STADIUMS).fetchall()


def get_all_past_stadiums(connection):
    """ Get all records in the 'past_stadiums' table 
    
    Args:
        connection:   Connection object

    Returns:
        All records in table
    """
    with connection:
        return connection.execute(GET_ALL_PAST_STADIUMS).fetchall()


def get_club_stadium_name(connection, club, year):
    """ Get stadium name of club at a given year / season
    
    Args:
        connection:     Connection object
        club:           Club e.g Liecester
        year:           Season year for example 1999

    Returns:
        Stadium name of club 'club_name'
    """
    stadium_name = get_club_past_stadium_name(connection, club, year)
    if stadium_name is not None:
        return stadium_name

    return get_club_present_stadium_name(connection, club)


def get_club_past_stadium_name(connection, club, year):
    """ Get past stadium name of club
    
    Args:
        connection:     Connection object
        club:           Club
        year:           Season year for example 1999

    Returns:
        Stadium name of club 'club_name'
    """
    with connection:
        return connection.execute(GET_CLUB_PAST_STADIUM_NAME, (club, year)).fetchone()


def get_club_present_stadium_name(connection, club):
    """ Get present stadium name of club
    
    Args:
        connection:     Connection object
        club_name:      Club name

    Returns:
        Stadium name of club 'club_name'
    """
    return connection.execute(GET_CLUB_PRESENT_STADIUM_NAME, (club,)).fetchone()


def present_stadiums_table_exist(connection):
    return footy_database.table_exist(connection, "present_stadiums")


def past_stadiums_table_exist(connection):
    return footy_database.table_exist(connection, "past_stadiums")


def drop_present_stadiums_table(connection):
    footy_database.drop_table(connection, "present_stadiums")


def drop_past_stadiums_table(connection):
    footy_database.drop_table(connection, "past_stadiums")










