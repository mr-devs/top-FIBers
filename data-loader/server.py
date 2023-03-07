from flask import Flask
from app import controller
import re
import os
import datetime

facebook_data_root = "../data/derived/fib_results/facebook/"
twitter_data_root = "../data/derived/fib_results/twitter/"
PLATFORMS = ["Facebook", "Twitter"]
LOAD_PAST_MONTH_DATA = ['2023_01']

def load_current_data():
    """
    Load each platform and read the files.
    """
    for platform in PLATFORMS:
        if platform == 'Facebook':
            read_dir = facebook_data_root
        else:
            read_dir = twitter_data_root
        all_year_month = get_available_year_month(read_dir)
        current_year_month = datetime.datetime.now().strftime("%Y_%m")
        selected_month = list(filter(lambda x: current_year_month in x, all_year_month))
        if len(selected_month) == 1:
            controller.read_files(read_dir, platform, selected_month[0])
        else:
            raise Exception("Error in finding data on", current_year_month)
            logger.error("Error in finding data on {}", current_year_month)

def load_past_data():
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

def get_available_year_month(root_dir):
    """
    Get available year and month
    """
    year_months = []
    for root_folder in os.listdir(root_dir):
        match = re.search(r'\d{4}_\d{2}', root_folder)
        if match is None:
            continue
        year_months.append(match.group())
    return year_months

if __name__ == '__main__':
    load_past_data()

