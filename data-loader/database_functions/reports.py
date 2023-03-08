"""
Purpose:
    This script used to add the data to reports table
Inputs:
    - The data need to be passed here are,
       |- date, report_name, platform
Outputs:
    The report id will be passed.

Authors: Pasan Kamburugamuwa
"""

import logging
from flask import Flask
from library import backend_util

app = Flask(__name__)

#Add report data to database
def add_reports(date, report_name, platform):
    logger.info("Add data to reports table")
    with backend_util.get_db_cursor() as cur:
        try:
            add_report = "INSERT INTO reports (date, name, platform) values (%s, %s, %s) RETURNING id"
            cur.execute(add_report, (date, report_name, platform))
            if cur.rowcount > 0:
                add_report = cur.fetchone()[0]
                result = {"id" : add_report}
            return result
        except Exception as ex:
            raise Exception(ex)

#check the report date is already in the database- report table
def check_report_already_added(date, report_name, platform):
    with backend_util.get_db_cursor() as cur:
        select_query = "SELECT id from reports where date= %s and name = %s and platform = %s;"
        cur.execute(select_query, (date, report_name, platform))
        if cur.rowcount > 0:
            result = False
        else:
            result = True
        return result
