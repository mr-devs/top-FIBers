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
from library.utils import get_logger

#get the absolute path of the facebook dir
facebook_data_root = os.path.abspath(os.path.join(os.getcwd(), "../data/derived/fib_results/facebook/"))
#get the abosolute path of the twitter dir
twitter_data_root = os.path.abspath(os.path.join(os.getcwd(),"../data/derived/fib_results/twitter/"))
PLATFORMS = ["Facebook", "Twitter"]
#to load the past months data(2022_01, 2022_02, 2022_04 ..) use this array
LOAD_PAST_MONTH_DATA = ['2022_01']

LOG_DIR = os.path.abspath(os.path.join(os.getcwd(), "../logs"))
LOG_FNAME = "data_loader_script.log"

def load_current_month_data():
    """
    Load each platform and read the files.
    """
    logger.info("Begin load current month data")
    for platform in PLATFORMS:
        if platform == 'Facebook':
            read_dir = facebook_data_root
        else:
            read_dir = twitter_data_root
        try:
           #get the current year_month
           current_year_month = datetime.datetime.now().strftime("%Y_%m")
           print(current_year_month)
           #call the read_file func in controller to read the file
           controller.read_files(read_dir, platform, current_year_month)
           logger.info(f"Successfully feed the data to the database on month of : {current_year_month}")
           logger.info("--------------------------------------------")
        except Exception:
           logger.exception(f"Error in adding data to the database on month : {current_year_month}")
           raise Exception(e)

def load_past_months_data():
    """
    Load each platform and read the files for past months. This function is
    used only once.
    """
    logger.info("Begin load past month data")
    for selected_month in LOAD_PAST_MONTH_DATA:
        for platform in PLATFORMS:
            if platform == 'Facebook':
                read_dir = facebook_data_root
            else:
                read_dir = twitter_data_root
            try:
                #read the past month data
                controller.read_files(read_dir, platform, selected_month)
                logger.info(f"Successfully feed the data to the database on month of : {current_year_month}")
                logger.info("--------------------------------------------")
            except Exception as e:
                logger.exception(f"Problem with adding data to the database with month: {selected_month}")
                raise Exception(e)

if __name__ == '__main__':
    script_name = os.path.basename(__file__)
    logger = get_logger(LOG_DIR, LOG_FNAME, script_name=script_name, also_print=True)
    logger.info("-" * 50)
    logger.info(f"Begin script: {__file__}")

    load_past_months_data()

