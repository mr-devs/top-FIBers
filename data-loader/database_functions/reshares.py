"""
Purpose:
    This script used to add the data to reshares table
Inputs:
    - The data need to be passed here for add_reshares,
       |- post_id, repord_id, platform, num_shares
Outputs:
    The post_id id will be passed.

Authors: Pasan Kamburugamuwa
"""

import logging
from flask import Flask
from library import backend_util

app = Flask(__name__)

#Add reshares data to table
def add_reshares(post_id, repord_id, platform, num_shares):
    with backend_util.get_db_cursor() as cur:
        try:
            add_reshare = "INSERT INTO reshares (post_id, report_id, platform, num_reshares) values (%s, %s, %s, %s) RETURNING post_id"
            cur.execute(add_reshare, (post_id, repord_id, platform, num_shares))
            if cur.rowcount > 0:
                post_fetch_id = cur.fetchone()[0]
                result = {"post_id" : post_fetch_id}
            return result
        except Exception as ex:
            raise Exception(ex)

#Get all reshares data
def get_all_reshares():
    all_reshares = []
    with backend_util.get_db_cursor() as cur:
        select_query = ("SELECT post_id, repord_id, platform, num_shares from reshares;")
        cur.execute(select_query)
        if cur.rowcount > 0:
            all_post_details = cur.fetchall()
            for post in all_post_details:
                post_json = {"post_id": post[0],
                             "repord_id": post[1],
                             "platform": post[2],
                             "platform": post[3],
                             }
                all_reshares.append(post_json)
    return all_reshares
