"""
Test the data module
Author: Jillian Ivie (iviej@my.erau.edu)
"""
from unittest import TestCase # to create individual test cases
from os.path import exists, join # to check if a given file path exists and combines parts of file path
from os import remove # to delete a file 
from data import fetch_data


class Test(TestCase):
    """ This class inherits from TestCase

    Args:
        TestCase
    """
    def test_data_acquisition(self):
        """
            This function fetches new data and performs basic checks
        """
        #create a file path and ensure correct construction
        path_to_data_file = join("src", "data", "weather.json")
        if exists(path_to_data_file):
            remove(path_to_data_file)
        #confirm file does not exist after potential removal
        assert False is exists(path_to_data_file)
        forecast = fetch_data(DATA_URL = "https://api.weather.gov/gridpoints/FGZ/152,54/forecast",
                            DATA_FILE = "./app/data/weather.json")
        assert exists(path_to_data_file)
        periods = forecast["properties"]["periods"]
        #check that periods list is not empty
        assert len(periods)
        #verify temperature data is present
        assert periods[0]["temperature"]
