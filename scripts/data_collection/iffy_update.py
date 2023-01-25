from urllib import request
import requests
import pandas as pd
import json
import sys


def get_iffy():
    """grab the latest version of iffy list and save to local"""
    url = 'https://iffynews.page.link/sheet'
    sheet_name = "Iffy-news"

    response = request.urlopen(url)
    new_url = response.geturl()
    sheet_id = new_url.split("/")[-2]
    google_url = "https://docs.google.com/spreadsheets/d/"+sheet_id+"/gviz/tq?tqx=out:csv&sheet="+sheet_name
    df = pd.read_csv(google_url)
    list_of_url = [x+"*"+"\n" for x in df.URL.tolist()]
    return list_of_url


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_iffy.py </path/to/file> \n Download the latest iffy list")
        exit()
    iffy_file = sys.argv[1]
    new_iffy = get_iffy()
    with open(iffy_file, "w+") as outfile:
        outfile.writelines(new_iffy)
