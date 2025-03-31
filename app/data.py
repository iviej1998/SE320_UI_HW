""" 
Obtain weather forecast for Saint Johns, Arizona
Author: Jillian Ivie
"""
#import modules
from requests import get
import streamlit as st
from json import dump, load
from dateutil import tz #managing time zones
from datetime import datetime #parsing and formatting date and time information

DATA_URL = "https://api.weather.gov/points/34.6164,-109.422" #set the API endpoint URL
DATA_FILE = "./app/data/weather.json" #define a path to save and read cached weather forecast data

headers = {
    "User-Agent": "SE320App (iviej@my.erau.edu)"
}

#decorate fetch_data function to tell streamlit to cache the function's output
#show_spinner: displays loading message
#ttl: sets time-to-live for the cache to 10 minutes
@st.cache_data(show_spinner="Fetching data from the API...", ttl = 60*10)
def fetch_data(DATA_URL:str, DATA_FILE:str) -> dict:
    """ This function fetches data from the API or from a file

    Args:
        DATA_URL (str)
        DATA_FILE (str)

    Returns:
        dict: dictionary containing forecast data
    """
    try: #attempt fetching and processing data while handling errors
        forecast = get(url=DATA_URL, timeout = 4).json() # send HTTP GET request to the URL w/a 3 second timeout
        if forecast and forecast.get("properties", {}).get("periods"):
            #save forecast to file as a backup
            with open(DATA_FILE, "w", encoding="utf-8") as file:
            # UTF-8 ensures correct handling of all characters
                dump(forecast,file)
                print("Data saved to weather.json", forecast)
                return forecast #after saving the forecast, return the forecast dictionary
            #if checking fails, attempt to open local file for reading
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                forecast = load(file) #deserialize JSON data and load into variable
                return forecast    
    #OSError: occurs during file operations or network issues
    except OSError as err:
        st.error(str(err), icon="💣") #error message is displayed in streamlit with error icon
    #TypeError: occurs when decoding JSON
    except TypeError as err:
        st.error(str(err), icon="💣")
    return {} #return empty dictionary upon failure

def reload_data() -> None:
    """ This function clears cached weather data
        The next call to fetch_data with force a fresh API request

    Args:
        None

    Returns:
        None
    """
    fetch_data.clear()
    
def last_updated(forecast: dict) -> str:
    """ This function returns the last update timestamp of the forecast data

    Args:
        forecast (dict)

    Returns:
        str: a formatted string 
    """
    try:
        #extract the "updateTime" from the forecast's properties
        #convert into a Python datetime object
        dtime = datetime.fromisoformat(forecast['properties']['updateTime'])
        #set timezone identifier to America/Arizona
        dtime = dtime.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz("MST"))
        #use strftime to format the datetime into a readable string
        return dtime.strftime('%A, %B %-d, %Y %-I:%M:%S %p %Z')
    except(KeyError, TypeError) as e:
        print(f"[last_updated] Error: {e} | forecast = {forecast}")
        return "Update time not available"
        