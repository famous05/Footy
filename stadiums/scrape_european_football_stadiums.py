# scrape_european_football_stadiums.py
#!/usr/bin/env python3

""" Python script to scrape european football clubs.

This module scrapes european football clubs data from 
https://www.stadiumguide.com and store data in the json files:
    - present_european_football_stadiums.json
    - past_european_football_stadiums.json


Available functions:
- extract_stadium_records: Extracts stadium records for each country.
- transform_stadium_records: Tranforms stadium records into python dictonary.
- load_to_json: Loads the data into a json file format.
...
"""

from bs4 import BeautifulSoup
import requests
import json

def extract_stadium_records(base_url, country):
    """ Extracts stadium record for a particular country. 
    
    Args:
        base_url:   Base url as part of country stadium data url name
        country:    Country to scrape stadium data for

    Returns:
        bs4 html list of stadiums
    """

    url = base_url + country + '/'
    html_text = requests.get(url).text
    soup  = BeautifulSoup(html_text, 'lxml')
    return soup.find_all('tr')[1:] # Ignore first item as it is the header


def transform_present_stadium_records(stadiums, country):
    """ Transform Beautiful soup present stadium record to python dictionary. 
    
    Args:
        stadiums:   bs4 html list of stadiums
        country:    Country of the stadiums        

    Returns:
        Dictionary of stadiums for the country
    """
  
    for stadium in stadiums:
        yield{
        'city' : stadium.find('td', class_='column-1').text,
        'club' : stadium.find('td', class_='column-2').text,
        'stadium_name' : stadium.find('a').text,
        'capacity': stadium.find('td', class_='column-4').text,
        'country': country
        }

def transform_past_stadium_records(stadiums, country):
    """ Transform Beautiful soup past stadium record to python dictionary. 
    
    Args:
        stadiums:   bs4 html list of stadiums
        country:    Country of the stadiums        

    Returns:
        Dictionary of stadiums for the country
    """
    for stadium in stadiums:
        yield{ 
        'club' : stadium.find('td', class_='column-2').text,
        'past_stadium_name' : stadium.find('a').text,
        'year_closed': stadium.find('td', class_='column-4').text
        }


def load_to_json(stadiums_list, json_file):
    """ Loads stadiums_list into json file. 
    
    Args:
        stadium_list:   List of dictionaries of stadium records
        json_file:      Output json file name
    """

    with open(json_file, 'w') as outfile:
        json.dump(stadiums_list, outfile)


def main():

    # Set up list of european countries to scrape stadiums information from
    # This list is based on Main Leagues in 'https://www.football-data.co.uk/data.php'
    #european_countries = ['England', 'Scotland', 'Germany', 'Italy', 'Spain', 
    #'Netherlands', 'Belgium', 'Portugal', 'Turkey', 'Greece', 'France']
    european_countries = ['England']

    # Process present european football clubs stadiums ########################
    base_url = 'https://www.stadiumguide.com/present/'
    stadiums_list = [] # List to hold unique stadium record
    for country in european_countries:
        stadiums = extract_stadium_records(base_url, country)
        stadiums = transform_present_stadium_records(stadiums, country)
        for stadium in stadiums:
            stadiums_list.append(stadium)

    load_to_json(stadiums_list, 'present_european_football_stadiums.json')
    ###########################################################################


    # Process past european football clubs stadiums ###########################
    # Updated countries list. Ommitted countries had no past stadiums data
    # and was causing error 
    # european_countries = ['England', 'Germany', 'Italy', 'Spain', 'Netherlands', 
    # 'Portugal', 'Greece']
    european_countries = ['England']
    base_url = 'https://www.stadiumguide.com/past/past-stadiums-'
    stadiums_list = [] # List to hold unique stadium record
    for country in european_countries:
        stadiums = extract_stadium_records(base_url, country)
        stadiums = transform_past_stadium_records(stadiums, country)
        for stadium in stadiums:
            stadiums_list.append(stadium)

    load_to_json(stadiums_list, 'past_european_football_stadiums.json')
    ###########################################################################


if __name__ == "__main__":
    main()




