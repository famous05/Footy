# process_european_football_stadiums_data.py
#!/usr/bin/env python3

""" Python script to process european football stadiums
    data produced by 'scrape_european_football_stadiums.py .

This module reads the following files:
    - present_european_football_stadiums.json
    - past_european_football_stadiums.json

and does the following:
    - combine into a single json and csv file
    - creates a sqlite db with two tables


Available functions:

...
"""

import pandas as pd
import json
import sqlite3
import os
import sys

import footy_database_stadiums

# Add parent directory to sys.path
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import footy_database

def main():

    # 1. COMBINE JSON files into one and write to JSON & CSV ##################

    # Read both json files into Pandas dataframes
    df_present = pd.read_json('present_european_football_stadiums.json')
    df_past = pd.read_json('past_european_football_stadiums.json')

    # Merge the df's
    frames = [df_present, df_past]
    result = pd.merge(df_present, df_past, how="left", on="club")

    # Replace Na's
    result["past_stadium_name"].fillna(result["stadium_name"], inplace=True)
    result["year_closed"].fillna(3000, inplace=True)

    # Write to JSON & CSV
    result.to_json('european_football_stadiums.json')
    result.to_csv('european_football_stadiums.csv')

    ###########################################################################


    # 2. SET UP SQLite DB #####################################################

    # Get database
    cwd = os.getcwd()
    os.chdir("../")
    database = os.getcwd() + "/" + "Footy.db"
    os.chdir(cwd)

    # Create a database connection
    #connection = footy_database_stadiums.create_connection(database)
    connection = footy_database.create_connection()

    # Create tables
    if connection is not None:
        footy_database_stadiums.create_present_stadiums_table(connection)
        footy_database_stadiums.create_past_stadiums_table(connection)
    else:
        print("Error! cannot create the database connection.")

    # TODO:
    # Find out it table was previously not there and was just created, then 
    # add the values, otherwise it is duplicated each time this script is executed

    # Add records to 'present_stadiums' table
    for ind in df_present.index:
        footy_database_stadiums.add_present_stadium(connection, 
        df_present['city'][ind], df_present['club'][ind], df_present['stadium_name'][ind], 
        df_present['capacity'][ind], df_present['country'][ind])

    # Add records to 'past_stadiums' table
    for ind in df_past.index:
        footy_database_stadiums.add_past_stadium(connection, 
        df_past['club'][ind], df_past['past_stadium_name'][ind], int(df_past['year_closed'][ind]))
    
    ###########################################################################

if __name__ == "__main__":
    main()

