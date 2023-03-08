"""
Purpose:
    This script fetch the current month data and feed the data in to database
Inputs:
    *No inputs to the function
    *If you need to run for the past months which is missed. use the LOAD_PAST_MONTH_DATA array
    *This script will grab the current year_month and execute it.
Output:
    *No output available, this will add data to database.
Author: Pasan Kamburugamuwa
"""

from flask import Flask
from app import controller
import re
import os
import datetime

#get the absolute path of the facebook dir
facebook_data_root = os.path.abspath(os.path.join(os.getcwd(), "../data/derived/fib_results/facebook/"))
#get the abosolute path of the twitter dir
twitter_data_root = os.path.abspath(os.path.join(os.getcwd(),"../data/derived/fib_results/twitter/"))
PLATFORMS = ["Facebook", "Twitter"]
#to load the past months data(2022_01, 2022_02, 2022_04 ..) use this array
LOAD_PAST_MONTH_DATA = ['2022_01']

def load_current_month_data():
    """
    Load each platform and read the files.
    """
    for platform in PLATFORMS:
        if platform == 'Facebook':
            read_dir = facebook_data_root
        else:
            read_dir = twitter_data_root
        try:
           #get the current year_month
           current_year_month = datetime.datetime.now().strftime("%Y_%m")
           current_year_month_dir = os.path.join(read_dir, current_year_month)
           try:
               #call the read_file func in controller to read the file
               controller.read_files(read_dir, platform, selected_month[0])
           except Exception as err:
               traceback.print_tb(err.__traceback__)
               logger.error("Error in adding data to database")
        except Exception as err:
           traceback.print_tb(err.__traceback__)
           logger.error("Error in finding data on {}",current_year_month)

def load_past_months_data():
    """
    Load each platform and read the files.
    """
    for selected_month in LOAD_PAST_MONTH_DATA:
        for platform in PLATFORMS:
            if platform == 'Facebook':
                read_dir = facebook_data_root
            else:
                read_dir = twitter_data_root
            controller.read_files(read_dir, platform, selected_month)

if __name__ == '__main__':
    load_past_months_data()

